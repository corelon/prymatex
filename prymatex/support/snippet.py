#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Snippte's module
"""
import re, logging
import uuid as uuidmodule

if __name__ == '__main__':
    import os, sys
    sys.path.append(os.path.abspath("."))
    
from prymatex.support.utils import compileRegexp, OPTION_CAPTURE_GROUP, OPTION_MULTILINE

from prymatex.support.bundle import PMXBundleItem, PMXRunningContext
from prymatex.support.processor import PMXSyntaxProcessor
from prymatex.support.syntax import PMXSyntax

SNIPPET_SYNTAX = { 
 'patterns': [{'captures': {'1': {'name': 'keyword.escape.snippet'}},
               'match': '\\\\(\\\\|\\$|`)',
               'name': 'constant.character.escape.snippet'},
              #Structures
              #TabStop
              {'captures': {'1': {'name': 'keyword.tabstop.snippet'},
                            '2': {'name': 'keyword.tabstop.snippet'}},
               'match': '\\$(\\d+)|\\${(\\d+)}',
               'name': 'structure.tabstop.snippet'},
              #Placeholder
              {'begin': '\\$\\{(\\d+):',
               'beginCaptures': {'1': {'name': 'keyword.placeholder.snippet'}},
               'contentName': 'string.default',
               'end': '\\}',
               'name': 'structure.placeholder.snippet',
               'patterns': [{'include': '$self'}]},
              #Transformation
              {'begin': '\\$\\{(\\d+)/',
               'beginCaptures': {'1': {'name': 'keyword.transformation.snippet'}},
               'contentName': 'string.regexp',
               'end': '\\}',
               'name': 'structure.transformation.snippet',
               'patterns': [{'include': '#escaped_char'},
                            {'include': '#substitution'}]},
              # Variables
              #TabStop
              {'match': '\\$([a-zA-Z_][a-zA-Z0-9_]*)|\\${([a-zA-Z_][a-zA-Z0-9_]*)}',
               'captures': {'1': {'name': 'string.env.snippet'}},
               'name': 'variable.tabstop.snippet'},
              #Placeholder
              {'begin': '\\$\\{([a-zA-Z_][a-zA-Z0-9_]*):',
               'beginCaptures': {'1': {'name': 'string.env.snippet'}},
               'contentName': 'string.default',
               'end': '\\}',
               'name': 'variable.placeholder.snippet',
               'patterns': [{'include': '$self'}]},
              #Transformation
              {'begin': '\\$\\{([a-zA-Z_][a-zA-Z0-9_]*)/',
               'beginCaptures': {'1': {'name': 'string.env.snippet'}},
               'contentName': 'string.regexp',
               'end': '\\}',
               'name': 'variable.transformation.snippet',
               'patterns': [{'include': '#escaped_char'},
                            {'include': '#substitution'}]},
               #Shell
              {'begin': '`',
               'end': '`',
               'contentName': 'string.script',
               'name': 'string.interpolated.shell.snippet'}],
 'repository': {'condition': {'begin': '\\(\\?(\\d):',
                              'beginCaptures': {'1': {'name': 'string.regexp.condition'}},
                              'contentName': 'text.condition',
                              'end': '\\)',
                              'name': 'meta.structure.condition.regexp',
                              'patterns': [{'include': '#escaped_cond'},
                                           {'begin': ':',
                                            'end': '(?=\\))',
                                            'contentName': 'otherwise.condition',
                                            'patterns': [{'include': '#escaped_cond'}]
                                            }]},
                'escaped_cond': {'captures': {'1': {'name': 'keyword.escape.condition'}},
                                 'match': '\\\\([/\\)])',
                                 'name': 'constant.character.escape.condition'},
                'escaped_char': {'match': '\\\\[/\\\\\\}\\{]',
                                 'name': 'constant.character.escape.regexp'},
                #'replacements': {'match': '\\$\\d|\\\\[uUILE]',
                #                 'name': 'string.regexp.replacement'},
                'substitution': {'begin': '/',
                                 'contentName': 'string.regexp.format',
                                 'end': '/([mg]?)/?',
                                 'endCaptures': {'1': {'name': 'string.regexp.options'}},
                                 'patterns': [{'include': '#escaped_char'},
                                              {'include': '#condition'}]}},
}

#Snippet Node Bases
class Node(object):
    def __init__(self, scope, parent = None):
        self.scope = scope
        self.parent = parent
        self.disable = False

    def open(self, scope, text):
        return self

    def close(self, scope, text):
        if scope == self.scope:
            return self.parent
        return self
    
    def reset(self):
        attrs = ['start', 'end', 'content']
        for attr in attrs:
            if hasattr(self, attr):
                delattr(self, attr)
    
    def __len__(self):
        if hasattr(self, 'start') and hasattr(self, 'end'):
            return self.end - self.start
        return 0
    
    def render(self, processor):
        pass
    
class NodeList(list):
    def __init__(self, scope, parent = None):
        super(NodeList, self).__init__()
        self.scope = scope
        self.parent = parent
        self.__disable = False

    @property
    def disable(self):
        return self.__disable
        
    @disable.setter
    def disable(self, value):
        self.__disable = value
        for child in self:
            child.disable = value
        
    def open(self, scope, text):
        node = self
        if scope == 'constant.character.escape.snippet':
            self.append(text)
        elif scope == 'structure.tabstop.snippet':
            self.append(text)
            node = StructureTabstop(scope, self)
            self.append(node)
        elif scope == 'structure.placeholder.snippet':
            self.append(text)
            node = StructurePlaceholder(scope, self)
            self.append(node)
        elif scope == 'structure.transformation.snippet':
            self.append(text)
            node = StructureTransformation(scope, self)
            self.append(node)
        elif scope == 'variable.tabstop.snippet':
            self.append(text)
            node = VariableTabstop(scope, self)
            self.append(node)
        elif scope == 'variable.placeholder.snippet':
            self.append(text)
            node = VariablePlaceholder(scope, self)
            self.append(node)
        elif scope == 'variable.transformation.snippet':
            self.append(text)
            node = VariableTransformation(scope, self)
            self.append(node)
        elif scope == 'string.interpolated.shell.snippet':
            self.append(text)
            node = Shell(scope, self)
            self.append(node)
        return node

    def close(self, scope, text):
        if scope == self.scope:
            return self.parent
        elif scope == 'keyword.escape.snippet':
            self.append(text)
        else:
            self.append(text)
        return self
    
    def reset(self):
        for child in self:
            child.reset()
        attrs = ['start', 'end', 'content']
        for attr in attrs:
            if hasattr(self, attr):
                delattr(self, attr)
    
    def __len__(self):
        if hasattr(self, 'start') and hasattr(self, 'end'):
            return self.end - self.start
        return 0
        
    def __unicode__(self):
        return u"".join([unicode(node) for node in self])
    
    def render(self, processor):
        for child in self:
            child.render(processor)
    
    def __contains__(self, element):
        for child in self:
            if child == element:
                return True
            elif isinstance(child, NodeList) and element in child:
                return True
        return False
    
    def append(self, element):
        if isinstance(element, (str, unicode)):
            element = TextNode(element, self)
        super(NodeList, self).append(element)

#Basic TextNode
class TextNode(Node):
    def __init__(self, text, parent = None):
        super(TextNode, self).__init__("string", parent)
        self.text = text.replace('\\n', '\n').replace('\\t', '\t')

    def __len__(self):
        return len(self.text)
    
    def __unicode__(self):
        return self.text
    
    def render(self, processor):
        processor.insertText(self.text.replace('\n', '\n' + processor.indentation).replace('\t', processor.tabreplacement))
    
#Snippet root
class Snippet(NodeList):
    def __init__(self, scope, snippetItem):
        super(Snippet, self).__init__(scope)
        self.snippetItem = snippetItem

    def render(self, processor):
        self.start = processor.cursorPosition()
        super(Snippet, self).render(processor)
        self.end = processor.cursorPosition()

#Snippet structures
class StructureTabstop(Node):
    def __init__(self, scope, parent = None):
        super(StructureTabstop, self).__init__(scope, parent)
        self.placeholder = None
        self.index = None

    def close(self, scope, text):
        node = self
        if scope == 'keyword.tabstop.snippet':
            self.index = int(text)
        else:
            return super(StructureTabstop, self).close(scope, text)
        return node

    def render(self, processor, mirror = False):
        self.start = processor.cursorPosition()
        if self.placeholder != None:
            self.placeholder.render(processor, mirror = True)
        else:
            if hasattr(self, 'content'):
                processor.insertText(self.content)
        self.end = processor.cursorPosition()
    
    def taborder(self, container):
        if type(container) == list:
            container.append(self)
        else:
            self.placeholder = container
        return container
        
    def setContent(self, content):
        self.content = content
    
class StructurePlaceholder(NodeList):
    def __init__(self, scope, parent = None):
        super(StructurePlaceholder, self).__init__(scope, parent)
        self.index = None
        self.placeholder = None
        
    def close(self, scope, text):
        node = self
        if scope == 'keyword.placeholder.snippet':
            self.index = int(text)
        else:
            return super(StructurePlaceholder, self).close(scope, text)
        return node
        
    def render(self, processor, mirror = False):
        if not mirror:
            self.start = processor.cursorPosition()
        if hasattr(self, 'content'):
            processor.insertText(self.content)
        elif self.placeholder != None:
            self.placeholder.render(processor)
        else:
            super(StructurePlaceholder, self).render(processor)
        if not mirror:
            self.end = processor.cursorPosition()
    
    def taborder(self, container):
        if type(container) == list and container:
            for element in container:
                element.placeholder = self
        elif isinstance(container, StructurePlaceholder):
            self.placeholder = container
            return container
        return self

    def setContent(self, content):
        #Pongo un contenido y se corto el arbol
        self.content = content
        self.disable = True
        
class StructureTransformation(Node):
    def __init__(self, scope, parent = None):
        super(StructureTransformation, self).__init__(scope, parent)
        self.placeholder = None
        self.index = None
        self.regexp = None
    
    def open(self, scope, text):
        node = self
        if scope == 'string.regexp':
            node = self.regexp = Regexp(scope, self)
        else:
            return super(StructureTransformation, self).open(scope, text)
        return node
        
    def close(self, scope, text):
        node = self
        if scope == 'keyword.transformation.snippet':
            self.index = int(text)
        else:
            return super(StructureTransformation, self).close(scope, text)
        return node
    
    def render(self, processor):
        processor.startTransformation(self.regexp)
        if self.placeholder != None:
            self.placeholder.render(processor, mirror = True)
        processor.endTransformation(self.regexp)
    
    def taborder(self, container):
        if type(container) == list:
            container.append(self)
        else:
            self.placeholder = container
        return container

#Snippet variables
class VariableTabstop(Node):
    def __init__(self, scope, parent = None):
        super(VariableTabstop, self).__init__(scope, parent)
        self.name = None

    def close(self, scope, text):
        node = self
        if scope == 'string.env.snippet':
            self.name = text
        else:
            return super(VariableTabstop, self).close(scope, text)
        return node
    
    def render(self, processor):
        environment = processor.environmentVariables()
        if self.name in environment:
            processor.insertText(environment[self.name])

class VariablePlaceholder(NodeList):
    def __init__(self, scope, parent = None):
        super(VariablePlaceholder, self).__init__(scope, parent)
        self.name = None

    def close(self, scope, text):
        node = self
        if scope == 'string.env.snippet':
            self.name = text
        else:
            return super(VariablePlaceholder, self).close(scope, text)
        return node
    
    def render(self, processor):
        self.start = processor.cursorPosition()
        environment = processor.environmentVariables()
        if self.name in environment:
            processor.insertText(environment[self.name])
        else:
            super(VariablePlaceholder, self).render(processor)
        self.end = processor.cursorPosition()
    
class VariableTransformation(Node):
    def __init__(self, scope, parent = None):
        super(VariableTransformation, self).__init__(scope, parent)
        self.name = None
        self.regexp = None

    def open(self, scope, text):
        node = self
        if scope == 'string.regexp':
            node = self.regexp = Regexp(scope, self)
        else:
            return super(VariableTransformation, self).open(scope, text)
        return node
        
    def close(self, scope, text):
        node = self
        if scope == 'string.env.snippet':
            self.name = text
        else:
            return super(VariableTransformation, self).close(scope, text)
        return node
    
    def render(self, processor):
        environment = processor.environmentVariables()
        if self.name in environment:
            text = self.regexp.transform(environment[self.name], processor)
            processor.insertText(text)

class Regexp(NodeList):
    _repl_re = compileRegexp(u"\$(?:(\d+)|g<(.+?)>)")
    
    def __init__(self, scope, parent = None):
        super(Regexp, self).__init__(scope, parent)
        self.pattern = ""
        self.options = None

    def open(self, scope, text):
        node = self
        if scope == 'string.regexp.format':
            self.pattern += text[:-1]
        elif scope == 'meta.structure.condition.regexp':
            self.append(text.replace('\\n', '\n').replace('\\t', '\t'))
            node = Condition(scope, self)
            self.append(node)
        elif scope == 'constant.character.escape.regexp':
            #Escape in pattern
            if isinstance(self.pattern, basestring):
                self.pattern += text
            else:
                self.append(text.replace('\\n', '\n').replace('\\t', '\t'))
        else:
            return super(Regexp, self).open(scope, text)
        return node

    def close(self, scope, text):
        node = self
        if scope == 'string.regexp.format':
            self.append(text)
        elif scope == 'string.regexp.options':
            self.options = text
        elif scope == 'constant.character.escape.regexp':
            #Escape in pattern
            if isinstance(self.pattern, basestring):
                self.pattern += text
            else:
                self.append(text)
        else:
            return super(Regexp, self).close(scope, text)
        return node
    
    @staticmethod
    def uppercase(text):
        titles = text.split('\u')
        if len(titles) > 1:
            text = "".join([titles[0]] + map(lambda txt: txt[0].upper() + txt[1:], titles[1:]))
        uppers = text.split('\U')
        if len(uppers) > 1:
            text = "".join([uppers[0]] + map(lambda txt: txt.find('\E') != -1 and txt[:txt.find('\E')].upper() + txt[txt.find('\E') + 2:] or txt.upper(), uppers ))
        return text

    @staticmethod
    def lowercase(text):
        lowers = text.split('\L')
        if len(lowers) > 1:
            text = "".join([lowers[0]] + map(lambda txt: txt.find('\E') != -1 and txt[:txt.find('\E')].lower() + txt[txt.find('\E') + 2:] or txt.lower(), lowers ))
        return text
    
    @staticmethod
    def prepare_replacement(text):
        repl = None
        def expand(m, template):
            def handle(match):
                numeric, named = match.groups()
                if numeric:
                    return m.group(int(numeric)) or ""
                return m.group(named) or ""
            return Regexp._repl_re.sub(handle, template)
        if '$' in text:
            repl = lambda m, r = text: expand(m, r)
        else:
            repl = lambda m, r = text: r
        return repl

    def transform(self, text, processor):
        flags = [OPTION_CAPTURE_GROUP]
        if self.option_multiline:
            flags.append(OPTION_MULTILINE)
        pattern = compileRegexp(unicode(self.pattern), flags)
        result = ""
        for child in self:
            if isinstance(child, TextNode):
                repl = self.prepare_replacement(unicode(child))
                result += pattern.sub(repl, text)
            elif isinstance(child, Condition):
                for match in pattern.finditer(text):
                    repl = child.index <= len(match.groups()) != None and child.insertion or child.otherwise
                    if repl != None:
                        repl = self.prepare_replacement(repl)
                        result += pattern.sub(repl, match.group(0))
                    if not self.option_global:
                        break
        if any(map(lambda r: result.find(r) != -1, ['\u', '\U'])):
            result = Regexp.uppercase(result)
        if any(map(lambda r: result.find(r) != -1, ['\L'])):
            result = Regexp.lowercase(result)
        return result.replace('\n', '\n' + processor.indentation).replace('\t', processor.tabreplacement)
    
    @property
    def option_global(self):
        return self.options != None and 'g' in self.options or False
    
    @property
    def option_multiline(self):
        return self.options != None and 'm' in self.options or False
    
class Shell(NodeList):    
    def close(self, scope, text):
        node = self
        if scope == 'string.script':
            self.append(text)
        else:
            return super(Shell, self).close(scope, text)
        return node
    
    @property
    def manager(self):
        if not hasattr(self, "_manager"):
            item = self
            while not isinstance(item, Snippet):
                item = item.parent
            self._manager = item.snippetItem.manager
        return self._manager
    
    def execute(self, processor):
        # TODO Migrar a runing context
        def afterExecute(context):
            self.content = context.outputValue.strip().replace('\n', '\n' + processor.indentation).replace('\t', processor.tabreplacement)
        with PMXRunningContext(self, unicode(self), processor.environmentVariables()) as context:
            context.asynchronous = False
            self.manager.runProcess(context, afterExecute)
        
    def render(self, processor):
        if not hasattr(self, 'content'):
            self.execute(processor)
        processor.insertText(self.content)

class Condition(Node):
    def __init__(self, scope, parent = None):
        super(Condition, self).__init__(scope, parent)
        self.index = None
        self.insertion = None
        self.otherwise = None
        self.current = ""
        
    def open(self, scope, text):
        node = self
        if scope == 'otherwise.condition':
            self.current += text[:-1].replace('\\n', '\n').replace('\\t', '\t')
            self.insertion = self.current
            self.current = ""
        elif scope == 'constant.character.escape.condition':
            self.current += text.replace('\\n', '\n').replace('\\t', '\t')
        else:
            return super(Condition, self).open(scope, text)
        return node
    
    def close(self, scope, text):
        node = self
        if scope == 'string.regexp.condition':
            self.index = int(text)
        elif scope == 'text.condition' and self.insertion == None:
            self.current += text.replace('\\n', '\n').replace('\\t', '\t')
            self.insertion = self.current
        elif scope == 'keyword.escape.condition':
            self.current += text.replace('\\n', '\n').replace('\\t', '\t')
        elif scope == 'otherwise.condition':
            self.current += text.replace('\\n', '\n').replace('\\t', '\t')
            self.otherwise = self.current
            self.current = ""
        else:
            return super(Condition, self).close(scope, text)
        return node
    
    def append(self, element):
        self.current += element.replace('\\n', '\n').replace('\\t', '\t')

class PMXSnippetSyntaxProcessor(PMXSyntaxProcessor):
    def __init__(self, snippetItem):
        self.current = None
        self.node = Snippet("root", snippetItem)
        self.taborder = {}

    def openTag(self, name, start):
        token = self.current[self.index:start]
        self.node = self.node.open(name, token)
        self.index = start
        
    def closeTag(self, name, end):
        token = self.current[self.index:end]
        self.node = self.node.close(name, token)
        if hasattr(self.node, 'index') and callable(getattr(self.node, 'taborder', None)):
            container = self.taborder.setdefault(self.node.index, [])
            if (self.node != container and self.node not in container):
                self.taborder[self.node.index] = self.node.taborder(container)
        self.index = end

    def beginLine(self, line):
        if self.current != None:
            if self.index != len(self.current):
                self.node.append(self.current[self.index:len(self.current)])
            self.node.append("\n")
        self.current = line
        self.index = 0
        
    def startParsing(self, name):
        self.node.open(name, "")

    def endParsing(self, name):
        token = self.current[self.index:len(self.current)]
        self.node.close(name, token)

class PMXSnippet(PMXBundleItem):
    KEYS = [ 'content', 'disableAutoIndent', 'inputPattern' ]
    TYPE = 'snippet'
    FOLDER = 'Snippets'
    EXTENSION = 'tmSnippet'
    PATTERNS = ['*.tmSnippet', '*.plist']
    parser = PMXSyntax(uuidmodule.uuid1(), dataHash = SNIPPET_SYNTAX)
    
    def __init__(self, uuid, dataHash):
        PMXBundleItem.__init__(self, uuid, dataHash)
        self.snippet = None                     #TODO: Poner un mejor nombre, este es el snippet compilado
    
    def load(self, dataHash):
        PMXBundleItem.load(self, dataHash)
        for key in PMXSnippet.KEYS:
            setattr(self, key, dataHash.get(key, None))
    
    @property
    def hash(self):
        dataHash = super(PMXSnippet, self).hash
        for key in PMXSnippet.KEYS:
            value = getattr(self, key)
            if value != None:
                dataHash[key] = value
        return dataHash
    
    def save(self, namespace):
        PMXBundleItem.save(self, namespace)
        self.snippet = None
    
    @property
    def ready(self):
        return self.snippet != None
    
    def compile(self):
        processor = PMXSnippetSyntaxProcessor(self)
        self.parser.parse(self.content, processor)
        self.snippet = processor.node
        self.addTaborder(processor.taborder)

    def execute(self, processor):
        if not self.ready:
            self.compile()
        self.reset()
        processor.startSnippet(self)
        self.render(processor)
        holder = self.next()
        if holder != None:
            processor.selectHolder(holder)
        else:
            processor.endSnippet(self)
    
    @property
    def start(self):
        if hasattr(self, 'snippet') and hasattr(self.snippet, 'start'):
            return self.snippet.start
        return 0
    
    @property    
    def end(self):
        if hasattr(self, 'snippet') and hasattr(self.snippet, 'end'):
            return self.snippet.end
        return 0
    
    def reset(self):
        self.index = -1
        self.snippet.disable = False
        self.snippet.reset()
    
    def render(self, processor):
        self.snippet.render(processor)
        
    def addTaborder(self, taborder):
        self.taborder = []
        lastHolder = taborder.pop(0, None)
        #TODO: ver si se puede sacar este "if pop" porque tendria que venir bien
        if type(lastHolder) == list:
            lastHolder = lastHolder.pop()
        keys = taborder.keys()
        keys.sort()
        for key in keys:
            holder = taborder.pop(key)
            if type(holder) == list:
                if len(holder) == 1:
                    holder = holder.pop()
                else:
                    #Esto puede dar un error pero me interesa ver si hay casos asi
                    tabstop = filter(lambda node: isinstance(node, StructureTabstop), holder).pop()
                    transformations = filter(lambda node: isinstance(node, StructureTransformation), holder)
                    for transformation in transformations:
                        transformation.placeholder = tabstop
                    holder = tabstop
            holder.last = False
            self.taborder.append(holder)
        if lastHolder is not None:
            lastHolder.last = True
        #elif self.taborder:
        #    self.taborder[-1].last = True
        self.taborder.append(lastHolder)
            

    def getHolder(self, start, end = None):
        ''' Return the placeholder for position, where starts > positiσn > ends'''
        end = end != None and end or start
        found = None
        for holder in self.taborder:
            # if holder == None then is the end of taborders
            if holder is None: break
            if holder.start <= start <= holder.end and holder.start <= end <= holder.end and (found == None or len(holder) < len(found)):
                found = holder
        return found
    
    def setCurrentHolder(self, holder):
        self.index = self.taborder.index(holder)
    
    def current(self):
        if self.index == -1:
            self.index = 0
        return self.taborder[self.index]

    def next(self):
        if self.index < len(self.taborder) - 1:
            self.index += 1
        #Fix disabled holders and None (last position in snippet)
        while self.index < len(self.taborder) - 1 and self.taborder[self.index] is not None and self.taborder[self.index].disable:
            self.index += 1
        return self.taborder[self.index]

    def previous(self):
        if self.index > 0:
            self.index -= 1
        while self.index != 0 and self.taborder[self.index].disable:
            self.index -= 1
        return self.taborder[self.index]
    
    def write(self, index, text):
        if index < len(self.taborder) and self.taborder[index] is not None and hasattr(self.taborder[index], "insert"):
            self.taborder[index].clear()
            self.taborder[index].insert(text, 0)
    
    def __len__(self):
        return len(self.taborder)
        
if __name__ == '__main__':
    content = """<div><ul>
    <li><a href="${1001}">${1002}</a></li>
    <li><a href="${1003}">${1004}</a></li>
    <li><a href="${1005}">${1006}</a></li>
    <li><a href="$1007">$1008</a></li>
    <li><a href="$1009">$1010</a></li>
    </ul></div>"""
    snippetHash = {    'content': content, 
                       'name': "MySnippet",
                 'tabTrigger': "MyTrigger",
              'keyEquivalent': None }
    snippet = PMXSnippet(uuidmodule.uuid1(), dataHash = snippetHash)
    snippet.compile()
    print(snippet.snippet)