#!/usr/bin/env python
#-*- encoding: utf-8 -*-

"""External Console"""

import sys
import os
import os.path as osp
import imp
import re

from prymatex.qt import QtGui, QtCore
from prymatex.qt.QtGui import (QVBoxLayout, QMessageBox, QInputDialog,
                                QLineEdit, QPushButton, QGroupBox, QLabel,
                                QTabWidget, QFontComboBox, QHBoxLayout)
from prymatex.qt.QtCore import SIGNAL, Qt
from prymatex.qt.compat import getOpenFileName
from prymatex.qt.helpers import create_action, mimedata2url

from prymatex import resources

# Local imports
from prymatex.core.config import _
from prymatex.utils import programs
from prymatex.utils.misc import (get_error_match, get_python_executable,
                                  remove_trailing_single_backslash)
from prymatex.widgets.tabs import Tabs
from prymatex.widgets.externalshell.pythonshell import ExternalPythonShell
from prymatex.widgets.externalshell.systemshell import ExternalSystemShell
from prymatex.core import PMXBaseDock

class ExternalConsole(QtGui.QDockWidget, PMXBaseDock):
    """External console widget"""
    SHORTCUT = "F9"
    ICON = resources.getIcon("console")
    PREFERED_AREA = QtCore.Qt.RightDockWidgetArea

    #=======================================================================
    # Settings
    #=======================================================================
    SETTINGS_GROUP = 'Console'
    def __init__(self, parent, light_mode = False):
        QtGui.QDockWidget.__init__(self, parent)
        PMXBaseDock.__init__(self)
        self.light_mode = light_mode
        self.tabwidget = None
        self.menu_actions = None
        
        self.inspector = None # Object inspector plugin
        self.historylog = None # History log plugin
        self.variableexplorer = None # Variable explorer plugin
        
        self.ipython_shell_count = 0
        self.python_count = 0
        self.terminal_count = 0

        
        if self.get_option('ipython_options', None) is None:
            self.set_option('ipython_options',
                            self.get_default_ipython_options())
        if self.get_option('ipython_kernel_options', None) is None:
            self.set_option('ipython_kernel_options',
                            self.get_default_ipython_kernel_options())
        
        executable = self.get_option('pythonexecutable',
                                     get_python_executable())
        if not osp.isfile(executable):
            # This is absolutely necessary, in case the Python interpreter
            # executable has been moved since last Spyder execution (following
            # a Python distribution upgrade for example)
            self.set_option('pythonexecutable', get_python_executable())
        elif executable.endswith('pythonw.exe'):
            # That should not be necessary because this case is already taken
            # care of by the `get_python_executable` function but, this was
            # implemented too late, so we have to fix it here too, in case
            # the Python executable has already been set with pythonw.exe:
            self.set_option('pythonexecutable',
                            executable.replace("pythonw.exe", "python.exe"))
        
        self.shellwidgets = []
        self.filenames = []
        self.icons = []
        self.runfile_args = ""
        
        self.tabwidget = Tabs(self, self.menu_actions)
        if hasattr(self.tabwidget, 'setDocumentMode')\
           and not sys.platform == 'darwin':
            self.tabwidget.setDocumentMode(True)
        self.connect(self.tabwidget, SIGNAL('currentChanged(int)'),
                     self.refresh_plugin)
        self.connect(self.tabwidget, SIGNAL('move_data(int,int)'),
                     self.move_tab)
                     
        self.tabwidget.set_close_function(self.close_console)

        # Find/replace widget
        #self.find_widget = FindReplace(self)
        #self.find_widget.hide()
        #self.register_widget_shortcuts("Editor", self.find_widget)
        
        #layout.addWidget(self.find_widget)
        
        self.setWidget(self.tabwidget)
            
        # Accepting drops
        self.setAcceptDrops(True)
        self.setWindowTitle(self.get_plugin_title())

    #------ PMXBaseDock API --------------------------------------------
    def initialize(self, mainWindow):
        PMXBaseDock.initialize(self, mainWindow)

    @classmethod
    def contributeToMainMenu(cls, addonClasses):
        interpreters = {
            'text': 'Interpreters',
            'items': [
                {'text': _('Open &interpreter'),
                 'icon': 'python',
                 'tip': _("Open a Python interpreter"),
                 'callback': cls.open_interpreter }
            ]}
        return { "Interpreters": interpreters }
                
    def move_tab(self, index_from, index_to):
        """
        Move tab (tabs themselves have already been moved by the tabwidget)
        """
        filename = self.filenames.pop(index_from)
        shell = self.shellwidgets.pop(index_from)
        icons = self.icons.pop(index_from)
        
        self.filenames.insert(index_to, filename)
        self.shellwidgets.insert(index_to, shell)
        self.icons.insert(index_to, icons)
        self.emit(SIGNAL('update_plugin_title()'))

    def get_shell_index_from_id(self, shell_id):
        """Return shellwidget index from id"""
        for index, shell in enumerate(self.shellwidgets):
            if id(shell) == shell_id:
                return index
        
    def close_console(self, index=None):
        """Close console tab from index or widget (or close current tab)"""
        if not self.tabwidget.count():
            return
        if index is None:
            index = self.tabwidget.currentIndex()
        self.tabwidget.widget(index).close()
        self.tabwidget.removeTab(index)
        self.filenames.pop(index)
        self.shellwidgets.pop(index)
        self.icons.pop(index)
        self.emit(SIGNAL('update_plugin_title()'))
        
    def set_variableexplorer(self, variableexplorer):
        """Set variable explorer plugin"""
        self.variableexplorer = variableexplorer
        
    def __find_python_shell(self, interpreter_only=False):
        current_index = self.tabwidget.currentIndex()
        if current_index == -1:
            return
        from spyderlib.widgets.externalshell import pythonshell
        for index in [current_index]+range(self.tabwidget.count()):
            shellwidget = self.tabwidget.widget(index)
            if isinstance(shellwidget, pythonshell.ExternalPythonShell):
                if interpreter_only and not shellwidget.is_interpreter:
                    continue
                elif not shellwidget.is_running():
                    continue
                else:
                    self.tabwidget.setCurrentIndex(index)
                    return shellwidget
                
    def get_running_python_shell(self):
        """
        Called by object inspector to retrieve a running Python shell instance
        """
        current_index = self.tabwidget.currentIndex()
        if current_index == -1:
            return
        from spyderlib.widgets.externalshell import pythonshell
        shellwidgets = [self.tabwidget.widget(index)
                        for index in range(self.tabwidget.count())]
        shellwidgets = [_w for _w in shellwidgets
                        if isinstance(_w, pythonshell.ExternalPythonShell) \
                        and _w.is_running()]
        if shellwidgets:
            # First, iterate on interpreters only:
            for shellwidget in shellwidgets:
                if shellwidget.is_interpreter:
                    return shellwidget.shell
            else:
                return shellwidgets[0].shell
        
    def run_script_in_current_shell(self, filename, wdir, args, debug):
        """Run script in current shell, if any"""
        line = "%s(r'%s'" % ('debugfile' if debug else 'runfile',
                             unicode(filename))
        norm = lambda text: remove_trailing_single_backslash(unicode(text))
        if args:
            line += ", args=r'%s'" % norm(args)
        if wdir:
            line += ", wdir=r'%s'" % norm(wdir)
        line += ")"
        self.execute_python_code(line, interpreter_only=True)
            
    def set_current_shell_working_directory(self, directory):
        """Set current shell working directory"""
        shellwidget = self.__find_python_shell()
        if shellwidget is not None:
            shellwidget.shell.set_cwd(unicode(directory))
        
    def execute_python_code(self, lines, interpreter_only=False):
        """Execute Python code in an already opened Python interpreter"""
        shellwidget = self.__find_python_shell(
                                        interpreter_only=interpreter_only)
        if shellwidget is not None:
            if shellwidget.is_ipython_kernel:
                #  IPython plugin
                ipython_widget = self.mainWindow.get_ipython_widget(id(shellwidget))
                ipython_widget.execute(unicode(lines))
                ipython_widget.setFocus()
            else:
                shellwidget.shell.execute_lines(unicode(lines))
                shellwidget.shell.setFocus()
            
    def pdb_has_stopped(self, fname, lineno, shell):
        """Python debugger has just stopped at frame (fname, lineno)"""
        self.emit(SIGNAL("edit_goto(QString,int,QString)"),
                  fname, lineno, '')
        shell.setFocus()
        
    def start(self, fname, wdir=None, args='', interact=False, debug=False,
              python=True, ipython_shell=False, ipython_kernel=False,
              python_args=''):
        """
        Start new console
        
        fname:
          string: filename of script to run
          None: open an interpreter
        wdir: working directory
        args: command line options of the Python script
        interact: inspect script interactively after its execution
        debug: run pdb
        python: True: Python interpreter, False: terminal
        ipython: True: IPython interpreter, False: Python interpreter
        python_args: additionnal Python interpreter command line options
                   (option "-u" is mandatory, see widgets.externalshell package)
        """
        # Note: fname is None <=> Python interpreter
        if fname is not None and not isinstance(fname, basestring):
            fname = unicode(fname)
        if wdir is not None and not isinstance(wdir, basestring):
            wdir = unicode(wdir)
        
        if fname is not None and fname in self.filenames:
            index = self.filenames.index(fname)
            if self.get_option('single_tab'):
                old_shell = self.shellwidgets[index]
                if old_shell.is_running():
                    answer = QMessageBox.question(self, self.get_plugin_title(),
                        _("%s is already running in a separate process.\n"
                          "Do you want to kill the process before starting "
                          "a new one?") % osp.basename(fname),
                        QMessageBox.Yes | QMessageBox.Cancel)
                    if answer == QMessageBox.Yes:
                        old_shell.process.kill()
                        old_shell.process.waitForFinished()
                    else:
                        return
                self.close_console(index)
        else:
            index = self.tabwidget.count()

        # Creating a new external shell
        #pythonpath = self.mainWindow.get_spyder_pythonpath()
        pythonpath = ""
        light_background = self.get_option('light_background')
        #show_elapsed_time = self.get_option('show_elapsed_time')
        show_elapsed_time = True
        if python:
            pythonexecutable = self.get_option('pythonexecutable')
            if self.get_option('pythonstartup/default', True):
                pythonstartup = None
            else:
                pythonstartup = self.get_option('pythonstartup', None)
            #monitor_enabled = self.get_option('monitor/enabled')
            monitor_enabled = True
            mpl_patch_enabled = self.get_option('matplotlib/patch')
            if self.get_option('matplotlib/backend/enabled'):
                mpl_backend = self.get_option('matplotlib/backend/value')
            else:
                mpl_backend = None
            ets_backend = self.get_option('ets_backend', 'qt4')
            qt_api = self.get_option('qt/api')
            if qt_api not in ('pyqt', 'pyside'):
                qt_api = None
            install_qt_inputhook = self.get_option('qt/install_inputhook')
            pyqt_api = self.get_option('pyqt/api_version', 0)
            ignore_sip_setapi_errors = self.get_option(
                                            'pyqt/ignore_sip_setapi_errors')
            merge_output_channels = self.get_option('merge_output_channels')
            colorize_sys_stderr = self.get_option('colorize_sys_stderr')
            umd_enabled = self.get_option('umd/enabled')
            #umd_namelist = self.get_option('umd/namelist')
            umd_namelist = []
            umd_verbose = self.get_option('umd/verbose')
            #ar_timeout = CONF.get('variable_explorer', 'autorefresh/timeout')
            #ar_state = CONF.get('variable_explorer', 'autorefresh')
            ar_timeout = 1000
            ar_state = True
            if self.light_mode:
                from spyderlib.plugins.variableexplorer import VariableExplorer
                sa_settings = VariableExplorer.get_settings()
            else:
                sa_settings = None
            shellwidget = ExternalPythonShell(self, fname, wdir,
                           interact, debug, path=pythonpath,
                           python_args=python_args,
                           ipython_shell=ipython_shell,
                           ipython_kernel=ipython_kernel,
                           arguments=args, stand_alone=sa_settings,
                           pythonstartup=pythonstartup,
                           pythonexecutable=pythonexecutable,
                           umd_enabled=umd_enabled, umd_namelist=umd_namelist,
                           umd_verbose=umd_verbose, ets_backend=ets_backend,
                           monitor_enabled=monitor_enabled,
                           mpl_patch_enabled=mpl_patch_enabled,
                           mpl_backend=mpl_backend,
                           qt_api=qt_api, pyqt_api=pyqt_api,
                           install_qt_inputhook=install_qt_inputhook,
                           ignore_sip_setapi_errors=ignore_sip_setapi_errors,
                           merge_output_channels=merge_output_channels,
                           colorize_sys_stderr=colorize_sys_stderr,
                           autorefresh_timeout=ar_timeout,
                           autorefresh_state=ar_state,
                           light_background=light_background,
                           menu_actions=self.menu_actions,
                           show_buttons_inside=False,
                           show_elapsed_time=show_elapsed_time)
            self.connect(shellwidget, SIGNAL('pdb(QString,int)'),
                         lambda fname, lineno, shell=shellwidget.shell:
                         self.pdb_has_stopped(fname, lineno, shell))
            #self.register_widget_shortcuts("Console", shellwidget.shell)
        else:
            if os.name == 'posix':
                cmd = 'gnome-terminal'
                args = []
                if programs.is_program_installed(cmd):
                    if wdir:
                        args.extend(['--working-directory=%s' % wdir])
                    programs.run_program(cmd, args)
                    return
                cmd = 'konsole'
                if programs.is_program_installed(cmd):
                    if wdir:
                        args.extend(['--workdir', wdir])
                    programs.run_program(cmd, args)
                    return
            shellwidget = ExternalSystemShell(self, wdir, path=pythonpath,
                                          light_background=light_background,
                                          menu_actions=self.menu_actions,
                                          show_buttons_inside=False,
                                          show_elapsed_time=show_elapsed_time)
        
        # Code completion / calltips
        shellwidget.shell.setMaximumBlockCount(
                                            self.get_option('max_line_count', 10) )
        #shellwidget.shell.set_font( self.get_plugin_font() )
        shellwidget.shell.toggle_wrap_mode( self.get_option('wrap') )
        shellwidget.shell.set_calltips( self.get_option('calltips') )
        shellwidget.shell.set_codecompletion_auto(
                            self.get_option('codecompletion/auto') )
        shellwidget.shell.set_codecompletion_case(
                            self.get_option('codecompletion/case_sensitive') )
        shellwidget.shell.set_codecompletion_single(
                            self.get_option('codecompletion/show_single') )
        shellwidget.shell.set_codecompletion_enter(
                            self.get_option('codecompletion/enter_key') )
        if python and self.inspector is not None:
            shellwidget.shell.set_inspector(self.inspector)
            shellwidget.shell.set_inspector_enabled(
                                            self.get_option('object_inspector'))
        if self.historylog is not None:
            self.historylog.add_history(shellwidget.shell.history_filename)
            self.connect(shellwidget.shell,
                         SIGNAL('append_to_history(QString,QString)'),
                         self.historylog.append_to_history)
        self.connect(shellwidget.shell, SIGNAL("go_to_error(QString)"),
                     self.go_to_error)
        self.connect(shellwidget.shell, SIGNAL("focus_changed()"),
                     lambda: self.emit(SIGNAL("focus_changed()")))
        if python:
            if self.mainWindow.currentEditor() is not None:
                self.connect(shellwidget, SIGNAL('open_file(QString,int)'),
                             self.open_file_in_spyder)
            if fname is None:
                if ipython_shell:
                    self.ipython_shell_count += 1
                    tab_name = "IPython %d" % self.ipython_shell_count
                    tab_icon1 = resources.getIcon('ipython.png')
                    tab_icon2 = resources.getIcon('ipython_t.png')
                elif ipython_kernel:
                    tab_name = "IPyKernel"
                    tab_icon1 = resources.getIcon('ipython.png')
                    tab_icon2 = resources.getIcon('ipython_t.png')
                    self.connect(shellwidget,
                                 SIGNAL('create_ipython_frontend(QString)'),
                                 lambda cf: self.create_ipython_frontend(
                                         cf, kernel_widget_id=id(shellwidget)))
                else:
                    self.python_count += 1
                    tab_name = "Python %d" % self.python_count
                    tab_icon1 = resources.getIcon('python.png')
                    tab_icon2 = resources.getIcon('python_t.png')
            else:
                tab_name = osp.basename(fname)
                tab_icon1 = resources.getIcon('run.png')
                tab_icon2 = resources.getIcon('terminated.png')
        else:
            fname = id(shellwidget)
            if os.name == 'nt':
                tab_name = _("Command Window")
            else:
                tab_name = _("Terminal")
            self.terminal_count += 1
            tab_name += (" %d" % self.terminal_count)
            tab_icon1 = resources.getIcon('cmdprompt.png')
            tab_icon2 = resources.getIcon('cmdprompt_t.png')
        self.shellwidgets.insert(index, shellwidget)
        self.filenames.insert(index, fname)
        self.icons.insert(index, (tab_icon1, tab_icon2))
        if index is None:
            index = self.tabwidget.addTab(shellwidget, tab_name)
        else:
            self.tabwidget.insertTab(index, shellwidget, tab_name)
        
        self.connect(shellwidget, SIGNAL("started()"),
                     lambda sid=id(shellwidget): self.process_started(sid))
        self.connect(shellwidget, SIGNAL("finished()"),
                     lambda sid=id(shellwidget): self.process_finished(sid))
        #self.find_widget.set_editor(shellwidget.shell)
        self.tabwidget.setTabToolTip(index, fname if wdir is None else wdir)
        self.tabwidget.setCurrentIndex(index)
        shellwidget.set_icontext_visible(self.get_option('show_icontext'))
        
        # Start process and give focus to console
        shellwidget.start_shell()
        shellwidget.shell.setFocus()
        
    def create_ipython_frontend(self, connection_file, kernel_widget_id):
        """Create a new IPython frontend connected to a kernel just started"""
        index = self.get_shell_index_from_id(kernel_widget_id)
        match = re.match('^kernel-(\d+).json', connection_file)
        if match is not None:  # should not fail, but we never know...
            text = unicode(self.tabwidget.tabText(index))
            name = "%s (%s)" % (text, match.groups()[0])
            self.tabwidget.setTabText(index, name)
        self.mainWindow.new_ipython_frontend(connection_file, kernel_widget_id)
        
    def open_file_in_spyder(self, fname, lineno):
        """Open file in Spyder's editor from remote process"""
        self.mainWindow.currentEditor().activateWindow()
        self.mainWindow.currentEditor().raise_()
        self.mainWindow.currentEditor().load(fname, lineno)
        
    #------ Private API -------------------------------------------------------
    def process_started(self, shell_id):
        index = self.get_shell_index_from_id(shell_id)
        shell = self.shellwidgets[index]
        icon, _icon = self.icons[index]
        self.tabwidget.setTabIcon(index, icon)
        if self.inspector is not None:
            self.inspector.set_shell(shell.shell)
        if self.variableexplorer is not None:
            self.variableexplorer.add_shellwidget(shell)
        
    def process_finished(self, shell_id):
        index = self.get_shell_index_from_id(shell_id)
        shell = self.shellwidgets[index]
        _icon, icon = self.icons[index]
        self.tabwidget.setTabIcon(index, icon)
        if self.inspector is not None:
            self.inspector.shell_terminated(shell.shell)
        if self.variableexplorer is not None:
            self.variableexplorer.remove_shellwidget(shell_id)
        
    #------ SpyderPluginWidget API --------------------------------------------
    # TODO Aca hay que hacer magia
    def get_plugin_title(self):
        """Return widget title"""
        title = _('Console')
        if self.filenames:
            index = self.tabwidget.currentIndex()
            fname = self.filenames[index]
            if fname:
                title += ' - '+unicode(fname)
        return title
    
    def get_focus_widget(self):
        """
        Return the widget to give focus to when
        this plugin's dockwidget is raised on top-level
        """
        return self.tabwidget.currentWidget()
        
    def get_plugin_actions(self):
        """Return a list of actions related to plugin"""
        interpreter_action = create_action(self,
                            _("Open &interpreter"), None,
                            'python.png', _("Open a Python interpreter"),
                            triggered=self.open_interpreter)
        if os.name == 'nt':
            text = _("Open &command prompt")
            tip = _("Open a Windows command prompt")
        else:
            text = _("Open &terminal")
            tip = _("Open a terminal window inside Spyder")
        terminal_action = create_action(self, text, None, 'cmdprompt.png', tip,
                                        triggered=self.open_terminal)
        run_action = create_action(self,
                            _("&Run..."), None,
                            'run_small.png', _("Run a Python script"),
                            triggered=self.run_script)

        interact_menu_actions = [interpreter_action]
        tools_menu_actions = [terminal_action]
        self.menu_actions = [interpreter_action, terminal_action, run_action]
        
        ipython_kernel_action = create_action(self,
                            _("Start a new IPython kernel"), None,
                            'ipython.png', triggered=self.start_ipython_kernel)
        if programs.is_module_installed('IPython', '>=0.12'):
            self.menu_actions.insert(1, ipython_kernel_action)
            interact_menu_actions.append(ipython_kernel_action)
        
        ipython_action = create_action(self,
                            _("Open IPython interpreter"), None,
                            'ipython.png',
                            _("Open an IPython interpreter"),
                            triggered=self.open_ipython)
        if programs.is_module_installed('IPython', '>=0.10'):
            self.menu_actions.insert(1, ipython_action)
            interact_menu_actions.append(ipython_action)
        
        self.mainWindow.interact_menu_actions += interact_menu_actions
        self.mainWindow.tools_menu_actions += tools_menu_actions
        
        return self.menu_actions+interact_menu_actions+tools_menu_actions
    
    def register_plugin(self):
        """Register plugin in Spyder's main window"""
        if self.mainWindow.light:
            self.mainWindow.setCentralWidget(self)
            self.mainWindow.widgetlist.append(self)
        else:
            self.mainWindow.add_dockwidget(self)
            self.inspector = self.mainWindow.inspector
            if self.inspector is not None:
                self.inspector.set_external_console(self)
            self.historylog = self.mainWindow.historylog
            self.connect(self, SIGNAL("edit_goto(QString,int,QString)"),
                         self.mainWindow.currentEditor().load)
            self.connect(self.mainWindow.currentEditor(),
                         SIGNAL('run_in_current_console(QString,QString,QString,bool)'),
                         self.run_script_in_current_shell)
            self.connect(self.mainWindow.currentEditor(), SIGNAL("open_dir(QString)"),
                         self.set_current_shell_working_directory)
            self.connect(self.mainWindow.workingdirectory,
                         SIGNAL("set_current_console_wd(QString)"),
                         self.set_current_shell_working_directory)
            self.connect(self, SIGNAL('focus_changed()'),
                         self.mainWindow.plugin_focus_changed)
            self.connect(self, SIGNAL('redirect_stdio(bool)'),
                         self.mainWindow.redirect_internalshell_stdio)
            expl = self.mainWindow.explorer
            if expl is not None:
                self.connect(expl, SIGNAL("open_terminal(QString)"),
                             self.open_terminal)
                self.connect(expl, SIGNAL("open_interpreter(QString)"),
                             self.open_interpreter)
                self.connect(expl, SIGNAL("open_ipython(QString)"),
                             self.open_ipython)
            pexpl = self.mainWindow.projectexplorer
            if pexpl is not None:
                self.connect(pexpl, SIGNAL("open_terminal(QString)"),
                             self.open_terminal)
                self.connect(pexpl, SIGNAL("open_interpreter(QString)"),
                             self.open_interpreter)
                self.connect(pexpl, SIGNAL("open_ipython(QString)"),
                             self.open_ipython)
        
    def closing_plugin(self, cancelable=False):
        """Perform actions before parent main window is closed"""
        for shellwidget in self.shellwidgets:
            shellwidget.close()
        return True
    
    def refresh_plugin(self):
        """Refresh tabwidget"""
        shellwidget = None
        if self.tabwidget.count():
            shellwidget = self.tabwidget.currentWidget()
            editor = shellwidget.shell
            editor.setFocus()
            widgets = [shellwidget.create_time_label(), 5
                       ]+shellwidget.get_toolbar_buttons()+[5]
        else:
            editor = None
            widgets = []
        #self.find_widget.set_editor(editor)
        self.tabwidget.set_corner_widgets({Qt.TopRightCorner: widgets})
        if shellwidget:
            shellwidget.update_time_label_visibility()
        self.emit(SIGNAL('update_plugin_title()'))
    
    def apply_plugin_settings(self, options):
        """Apply configuration file's plugin settings"""
        whitebg_n = 'light_background'
        ipybg_n = 'ipython_set_color'
        if (whitebg_n in options or ipybg_n in options) \
           and self.get_option(ipybg_n):
            ipython_n = 'ipython_options'
            args = self.get_option(ipython_n, "")
            if args:
                lbgo = "-colors LightBG"
                if self.get_option(whitebg_n):
                    # White background
                    if lbgo not in args:
                        self.set_option(ipython_n, args+" "+lbgo)
                else:
                    # Black background
                    self.set_option(ipython_n, args.replace(" "+lbgo, ""
                                    ).replace(lbgo+" ", "").replace(lbgo, ""))
            else:
                lbgo = "-colors LightBG"
                if self.get_option(whitebg_n):
                    self.set_option(ipython_n, lbgo)
        
        font = self.get_plugin_font()
        showtime = self.get_option('show_elapsed_time')
        icontext = self.get_option('show_icontext')
        calltips = self.get_option('calltips')
        inspector = self.get_option('object_inspector')
        wrap = self.get_option('wrap')
        compauto = self.get_option('codecompletion/auto')
        case_comp = self.get_option('codecompletion/case_sensitive')
        show_single = self.get_option('codecompletion/show_single')
        compenter = self.get_option('codecompletion/enter_key')
        mlc = self.get_option('max_line_count')
        for shellwidget in self.shellwidgets:
            shellwidget.shell.set_font(font)
            shellwidget.set_elapsed_time_visible(showtime)
            shellwidget.set_icontext_visible(icontext)
            shellwidget.shell.set_calltips(calltips)
            if isinstance(shellwidget.shell, ExternalPythonShell):
                shellwidget.shell.set_inspector_enabled(inspector)
            shellwidget.shell.toggle_wrap_mode(wrap)
            shellwidget.shell.set_codecompletion_auto(compauto)
            shellwidget.shell.set_codecompletion_case(case_comp)
            shellwidget.shell.set_codecompletion_single(show_single)
            shellwidget.shell.set_codecompletion_enter(compenter)
            shellwidget.shell.setMaximumBlockCount(mlc)
    
    def set_option(self, option, value):
        self.settings.setValue(option, value)

    def get_option(self, option, default = None):
        value = self.settings.value(option, default)
        print option, value, default
        return value
        return self.settings.value(option, default)
    
    #------ Public API ---------------------------------------------------------
    def open_interpreter_at_startup(self):
        """Open an interpreter at startup, IPython if module is available"""
        if self.get_option('open_ipython_at_startup', False):
            if programs.is_module_installed('IPython', '0.10'):
                # IPython v0.10.x is fully supported by Spyder, not v0.11+
                self.open_ipython()
            else:
                # If IPython v0.11+ is installed (or if IPython is not
                # installed at all), we must -at least the first time- force
                # the user to start with the standard Python interpreter which
                # has been enhanced to support most of the IPython features
                # needed within an advanced IDE as Spyder:
                # http://spyder-ide.blogspot.com/2011/09/new-enhanced-scientific-python.html
                # The main motivation here is to be sure that the novice user
                # will have an experience as close as possible to MATLAB with
                # a ready-to-use interpreter with standard scientific modules
                # preloaded and with non-blocking interactive plotting.
                self.set_option('open_ipython_at_startup', False)
                self.set_option('open_python_at_startup', True)
        if self.get_option('open_python_at_startup', True):
            self.open_interpreter()
        if self.get_option('start_ipython_kernel_at_startup', False):
            self.start_ipython_kernel()
            
    def open_interpreter(self, wdir=None):
        """Open interpreter"""
        if wdir is None:
            wdir = os.getcwdu()
        self.start(fname=None, wdir=unicode(wdir), args='',
                   interact=True, debug=False, python=True)
        
    def get_default_ipython_options(self):
        """Return default ipython command line arguments"""
        default_options = []
        if programs.is_module_installed('matplotlib'):
            default_options.append("-pylab")
        default_options.append("-q4thread")
        default_options.append("-colors LightBG")
        default_options.append("-xmode Plain")
        for editor_name in ("scite", "gedit"):
            path = programs.find_program(editor_name)
            if path is not None:
                default_options.append("-editor "+osp.basename(path))
                break
        return " ".join(default_options)
        
    def get_default_ipython_kernel_options(self):
        """Return default ipython kernel command line arguments"""
        default_options = []
        if programs.is_module_installed('matplotlib'):
            default_options.append("--pylab=inline")
        return " ".join(default_options)
        
    def open_ipython(self, wdir=None):
        """Open IPython"""
        if wdir is None:
            wdir = os.getcwdu()
        args = self.get_option('ipython_options', "")
        self.start(fname=None, wdir=unicode(wdir), args=args,
                   interact=True, debug=False, python=True, ipython_shell=True)

    def start_ipython_kernel(self, wdir=None):
        """Start new IPython kernel"""
        if wdir is None:
            wdir = os.getcwdu()
        args = self.get_option('ipython_kernel_options',
                               "--pylab=inline")
        self.start(fname=None, wdir=unicode(wdir), args=args,
                   interact=True, debug=False, python=True,
                   ipython_kernel=True)

    def open_terminal(self, wdir=None):
        """Open terminal"""
        if wdir is None:
            wdir = os.getcwdu()
        self.start(fname=None, wdir=unicode(wdir), args='',
                   interact=True, debug=False, python=False)
        
    def run_script(self):
        """Run a Python script"""
        self.emit(SIGNAL('redirect_stdio(bool)'), False)
        filename, _selfilter = getopenfilename(self, _("Run Python script"),
                os.getcwdu(), _("Python scripts")+" (*.py ; *.pyw ; *.ipy)")
        self.emit(SIGNAL('redirect_stdio(bool)'), True)
        if filename:
            self.start(fname=filename, wdir=None, args='',
                       interact=False, debug=False)
        
    def set_umd_namelist(self):
        """Set UMD excluded modules name list"""
        arguments, valid = QInputDialog.getText(self, _('UMD'),
                                  _('UMD excluded modules:\n'
                                          '(example: guidata, guiqwt)'),
                                  QLineEdit.Normal,
                                  ", ".join(self.get_option('umd/namelist')))
        if valid:
            arguments = unicode(arguments)
            if arguments:
                namelist = arguments.replace(' ', '').split(',')
                fixed_namelist = [module_name for module_name in namelist
                                  if programs.is_module_installed(module_name)]
                invalid = ", ".join(set(namelist)-set(fixed_namelist))
                if invalid:
                    QMessageBox.warning(self, _('UMD'),
                                        _("The following modules are not "
                                          "installed on your machine:\n%s"
                                          ) % invalid, QMessageBox.Ok)
                QMessageBox.information(self, _('UMD'),
                                    _("Please note that these changes will "
                                      "be applied only to new Python/IPython "
                                      "interpreters"), QMessageBox.Ok)
            else:
                fixed_namelist = []
            self.set_option('umd/namelist', fixed_namelist)
        
    def go_to_error(self, text):
        """Go to error if relevant"""
        match = get_error_match(unicode(text))
        if match:
            fname, lnb = match.groups()
            self.emit(SIGNAL("edit_goto(QString,int,QString)"),
                      osp.abspath(fname), int(lnb), '')
            
    #----Drag and drop
    def __is_python_script(self, qstr):
        """Is it a valid Python script?"""
        fname = unicode(qstr)
        return osp.isfile(fname) and \
               ( fname.endswith('.py') or fname.endswith('.pyw') \
                 or fname.endswith('.ipy') )
        
    def dragEnterEvent(self, event):
        """Reimplement Qt method
        Inform Qt about the types of data that the widget accepts"""
        source = event.mimeData()
        if source.hasUrls():
            if mimedata2url(source):
                pathlist = mimedata2url(source)
                shellwidget = self.tabwidget.currentWidget()
                if all([self.__is_python_script(qstr) for qstr in pathlist]):
                    event.acceptProposedAction()
                elif shellwidget is None or not shellwidget.is_running():
                    event.ignore()
                else:
                    event.acceptProposedAction()
            else:
                event.ignore()
        elif source.hasText():
            event.acceptProposedAction()            
            
    def dropEvent(self, event):
        """Reimplement Qt method
        Unpack dropped data and handle it"""
        source = event.mimeData()
        shellwidget = self.tabwidget.currentWidget()
        if source.hasText():
            qstr = source.text()
            if self.__is_python_script(qstr):
                self.start(qstr)
            elif shellwidget:
                shellwidget.shell.insert_text(qstr)
        elif source.hasUrls():
            pathlist = mimedata2url(source)
            if all([self.__is_python_script(qstr) for qstr in pathlist]):
                for fname in pathlist:
                    self.start(fname)
            elif shellwidget:
                shellwidget.shell.drop_pathlist(pathlist)
        event.acceptProposedAction()

