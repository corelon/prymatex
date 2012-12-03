#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Running programs utilities
This code was adapted from spyderlib original developed by Pierre Raybaut
spyderlib site:
http://code.google.com/p/spyderlib
"""

import os
import os.path as osp
import sys
import subprocess
import imp
import re

from prymatex.utils import encoding

def is_program_installed(basename):
    """Return program absolute path if installed in PATH
    Otherwise, return None"""
    for path in os.environ["PATH"].split(os.pathsep):
        abspath = osp.join(path, basename)
        if osp.isfile(abspath):
            return abspath


def find_program(basename):
    """Find program in PATH and return absolute path
    Try adding .exe or .bat to basename on Windows platforms
    (return None if not found)"""
    names = [basename]
    if os.name == 'nt':
        # Windows platforms
        extensions = ('.exe', '.bat', '.cmd')
        if not basename.endswith(extensions):
            names = [basename+ext for ext in extensions]+[basename]
    for name in names:
        path = is_program_installed(name)
        if path:
            return path


def run_program(name, args=[], cwd=None):
    """Run program in a separate process"""
    assert isinstance(args, (tuple, list))
    path = find_program(name)
    if not path:
        raise RuntimeError("Program %s was not found" % name)
    subprocess.Popen([path]+args, cwd=cwd)


def start_file(filename):
    """Generalized os.startfile for all platforms supported by Qt
    (this function is simply wrapping QDesktopServices.openUrl)
    Returns True if successfull, otherwise returns False."""
    from spyderlib.qt.QtGui import QDesktopServices
    from spyderlib.qt.QtCore import QUrl
    url = QUrl()
    url.setUrl(filename)
    return QDesktopServices.openUrl(url)


def python_script_exists(package=None, module=None):
    """Return absolute path if Python script exists (otherwise, return None)
    package=None -> module is in sys.path (standard library modules)"""
    assert module is not None
    try:
        if package is None:
            path = imp.find_module(module)[1]
        else:
            path = osp.join(imp.find_module(package)[1], module)+'.py'
    except ImportError:
        return
    if not osp.isfile(path):
        path += 'w'
    if osp.isfile(path):
        return path


def run_python_script(package=None, module=None, args=[], p_args=[]):
    """Run Python script in a separate process
    package=None -> module is in sys.path (standard library modules)"""
    assert module is not None
    assert isinstance(args, (tuple, list)) and isinstance(p_args, (tuple, list))
    path = python_script_exists(package, module)
    subprocess.Popen([sys.executable]+p_args+[path]+args)


def shell_split(text):
    """Split the string `text` using shell-like syntax
    
    This avoids breaking single/double-quoted strings (e.g. containing 
    strings with spaces). This function is almost equivalent to the shlex.split
    function (see standard library `shlex`) except that it is supporting 
    unicode strings (shlex does not support unicode until Python 2.7.3)."""
    assert isinstance(text, basestring)  # in case a QString is passed...
    pattern = r'(\s+|(?<!\\)".*?(?<!\\)"|(?<!\\)\'.*?(?<!\\)\')'
    out = []
    for token in re.split(pattern, text):
        if token.strip():
            out.append(token.strip('"').strip("'"))
    return out


def get_python_args(fname, python_args, interact, debug, end_args):
    """Construct Python interpreter arguments"""
    p_args = []
    if python_args is not None:
        p_args += python_args.split()
    if interact:
        p_args.append('-i')
    if debug:
        p_args.extend(['-m', 'pdb'])
    if fname is not None:
        if os.name == 'nt' and debug:
            # When calling pdb on Windows, one has to replace backslashes by
            # slashes to avoid confusion with escape characters (otherwise, 
            # for example, '\t' will be interpreted as a tabulation):
            p_args.append(osp.normpath(fname).replace(os.sep, '/'))
        else:
            p_args.append(fname)
    if end_args:
        p_args.extend(shell_split(end_args))
    return p_args


def run_python_script_in_terminal(fname, wdir, args, interact,
                                  debug, python_args):
    """Run Python script in an external system terminal"""
    
    # If fname has spaces on it it can't be ran on Windows, so we have to
    # enclose it in quotes
    if os.name == 'nt':
        fname = '"' + fname + '"'
    
    p_args = ['python']
    p_args += get_python_args(fname, python_args, interact, debug, args)
    
    if os.name == 'nt':
        # Command line and cwd have to be converted to the filesystem
        # encoding before passing them to subprocess
        # See http://bugs.python.org/issue1759845#msg74142
        cmd = encoding.to_fs_from_unicode(
                'start cmd.exe /c "cd %s && ' % wdir + ' '.join(p_args) + '"')
        subprocess.Popen(cmd, shell=True,
                         cwd=encoding.to_fs_from_unicode(wdir))
    elif os.name == 'posix':
        cmd = 'gnome-terminal'
        if is_program_installed(cmd):
            run_program(cmd, ['--working-directory', wdir, '-x'] + p_args,
                        cwd=wdir)
            return
        cmd = 'konsole'
        if is_program_installed(cmd):
            run_program(cmd, ['--workdir', wdir, '-e'] + p_args,
                        cwd=wdir)
            return
        # TODO: Add a fallback to xterm for Linux and the necessary code for
        #       OSX
    else:
        raise NotImplementedError


def is_module_installed(module_name, version=None):
    """Return True if module *module_name* is installed
    
    If version is not None, checking module version 
    (module must have an attribute named '__version__')
    
    version may starts with =, >= or > to specify the exact requirement"""
    try:
        mod = __import__(module_name)
        if version is None:
            return True
        else:
            match = re.search('[0-9]', version)
            assert match is not None, "Invalid version number"
            symb = version[:match.start()]
            if not symb:
                symb = '='
            assert symb in ('>=', '>', '='),\
                   "Invalid version condition '%s'" % symb
            version = version[match.start():]
            try:
                actver = getattr(mod, '__version__',
                                 getattr(mod, 'VERSION', None))
            except AttributeError:
                return False
            def getvlist(version):
                """Return an integer list from a version string"""
                vl = version.split('.')
                while vl and not vl[-1].isdigit():
                    vl = vl[:-1]
                return [int(nb) for nb in vl]
            vlist = getvlist(version)
            actvlist = getvlist(actver)
            actvlist = actvlist[:len(vlist)]
            vlist = vlist[:len(actvlist)]
            if not vlist or not actvlist:
                return False
            for index, (nb, actnb) in enumerate(zip(vlist, actvlist)):
                if nb == actnb:
                    if index == len(vlist)-1 and '=' not in symb:
                        return False
                    else:
                        continue
                elif actnb < nb:
                    return False
                elif actnb > nb and symb == '=':
                    return False
            else:
                return True
    except ImportError:
        return False


if __name__ == '__main__':
    print(find_program('git'))
    print(shell_split('-q -o -a'))
    print(shell_split(u'-q "d:\\Python de xxxx\\t.txt" -o -a'))
