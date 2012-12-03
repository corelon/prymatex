#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Syntax's module
http://manual.macromates.com/en/language_grammars.html
http://manual.macromates.com/en/navigation_overview#customizing_foldings.html
"""

import re

from prymatex.support.bundle import PMXBundleItem
from prymatex.support.utils import compileRegexp
    
SPLITLINES = re.compile('\n')

class PMXSyntaxNode(object):
    def __init__(self, dataHash, syntax):
        for k in [  'syntax', 'match', 'begin', 'content', 'name', 'contentName', 'end',
                    'captures', 'beginCaptures', 'endCaptures', 'repository', 'patterns']:
            setattr(self, k, None)
        self.syntax = syntax
        for key, value in dataHash.iteritems():
            try:
                if key in ['match', 'begin']:
                    setattr(self, key, compileRegexp( value ))
                elif key in ['content', 'name', 'contentName', 'end']:
                    setattr(self, key, value )
                elif key in ['captures', 'beginCaptures', 'endCaptures']:
                    value = sorted(value.items(), key=lambda v: int(v[0]))
                    setattr(self, key, value)
                elif key == 'repository':
                    self.parse_repository(value)
                elif key in ['patterns']:
                    self.create_children(value)
            except TypeError, e:
                #an encoding can only be given for non-unicode patterns
                print(e, value)
    
    def parse_repository(self, repository):
        self.repository = {}
        for key, value in repository.iteritems():
            if 'include' in value:
                self.repository[key] = PMXSyntaxProxy( value, self.syntax )
            else:
                self.repository[key] = PMXSyntaxNode( value, self.syntax )

    def create_children(self, patterns):
        self.patterns = []
        for p in patterns:
            if 'include' in p:
                self.patterns.append(PMXSyntaxProxy( p, self.syntax ))
            else:
                self.patterns.append(PMXSyntaxNode( p, self.syntax ))
    
    def parse_captures(self, name, pattern, match, processor):
        captures = pattern.match_captures( name, match )
        #Aca tengo que comparar con -1, Ver nota en match_captures
        captures = filter(lambda (group, range, name): range != -1 and range[0] != range[-1], captures)
        starts = []
        ends = []
        for group, range, name in captures:
            starts.append([range[0], group, name])
            ends.append([range[-1], -group, name])
        starts = starts[::-1]
        ends = ends[::-1]
        
        while starts or ends:
            if starts:
                pos, _, name = starts.pop()
                processor.openTag(name, pos)
            elif ends:
                pos, _, name = ends.pop()
                processor.closeTag(name, pos)
            elif abs(ends[-1][1]) < starts[-1][1]:
                pos, _, name = ends.pop()
                processor.closeTag(name, pos)
            else:
                pos, _, name = starts.pop()
                processor.openTag(name, pos)
    
    def match_captures(self, name, match):
        matches = []
        captures = getattr(self, name)
        
        if captures:
            for key, value in captures:
                if re.compile('^\d*$').match(key):
                    if int(key) <= len(match.groups()):
                        #Problemas entre pytgon y ruby, al pones un span del match, en un None oniguruma me retorna (-1, -1),
                        #esto es importante para el filtro del llamador
                        matches.append([int(key), match.span(int(key)), value['name']])
                else:
                    if match.groups()[ key ]:
                        matches.append([match.groups()[ key ], match.groupdict[ key ], value['name']])
        return matches
      
    def match_first(self, string, position):
        if self.match:
            match = self.match.search( string, position )
            if match:
                return (self, match)
        elif self.begin:
            match = self.begin.search( string, position )
            if match:
                return (self, match) 
        elif self.end:
            pass
        else:
            return self.match_first_son( string, position )
        return (None, None)
    
    def match_end(self, string, match, position):
        regstring = self.end[:]
        def g_match(mobj):
            index = int(mobj.group(0)[1:])
            return match.group(index)
        def d_match(mobj):
            print("d_match")
            index = mobj.group(0)
            return match.groupdict[index]
        regstring = compileRegexp(u'\\\\([1-9])').sub(g_match, regstring)
        regstring = compileRegexp(u'\\\\k<(.*?)>').sub(d_match, regstring)
        return compileRegexp( regstring ).search( string, position )
    
    def match_first_son(self, string, position):
        match = (None, None)
        if self.patterns:
            for p in self.patterns:
                tmatch = p.match_first(string, position)
                if tmatch[1]:
                    if not match[1] or match[1].start() > tmatch[1].start():
                        match = tmatch
        return match

class PMXSyntaxProxy(object):
    def __init__(self, dataHash, syntax):
        self.syntax = syntax
        self.proxy = dataHash['include']
    
    def __getattr__(self, name):
        if self.proxy:
            proxy_value = self.__proxy()
            if proxy_value:
                return getattr(proxy_value, name)
    
    def __proxy(self):
        if re.compile('^#').search(self.proxy):
            grammar = self.syntax.grammar
            if hasattr(grammar, 'repository') and grammar.repository.has_key(self.proxy[1:]):  
                return grammar.repository[self.proxy[1:]]
        elif self.proxy == '$self':
            return self.syntax.grammar
        elif self.proxy == '$base':
            return self.syntax.grammar
        else:
            syntaxes = self.syntax.syntaxes
            if self.proxy in syntaxes:
                return syntaxes[self.proxy].grammar
            else:
                return PMXSyntaxNode({}, self.syntax)

class PMXSyntax(PMXBundleItem):
    KEYS = [ 'comment', 'firstLineMatch', 'foldingStartMarker', 'scopeName', 'repository', 'foldingStopMarker', 'fileTypes', 'patterns']
    TYPE = 'syntax'
    FOLDER = 'Syntaxes'
    EXTENSION = 'tmLanguage'
    PATTERNS = ['*.tmLanguage', '*.plist']
    FOLDING_NONE = 0
    FOLDING_START = 1
    FOLDING_STOP = -1
    ROOT_GROUPS = [ "comment", "constant", "entity", "invalid",
                    "keyword", "markup", "meta", "storage",
                    "string", "support", "variable" ]
    def load(self, dataHash):
        super(PMXSyntax, self).load(dataHash)
        for key in PMXSyntax.KEYS:
            value = dataHash.get(key, None)
            if value != None and key in ['firstLineMatch', 'foldingStartMarker', 'foldingStopMarker']:
                try:
                    value = compileRegexp( value )
                except TypeError, e:
                    value = None
                    print(self.name, key, e)
            setattr(self, key, value)
    
    @property
    def hash(self):
        dataHash = super(PMXSyntax, self).hash
        for key in PMXSyntax.KEYS:
            value = getattr(self, key)
            if value != None:
                if key in ['firstLineMatch', 'foldingStartMarker', 'foldingStopMarker']:
                    value = value.pattern
                dataHash[key] = value
        return dataHash

    @property
    def indentSensitive(self):
        #If stop marker match with "" the grammar is indent sensitive
        match = self.foldingStopMarker.search("") if self.foldingStopMarker != None else None
        return match != None

    @property
    def syntaxes(self):
        return self.manager.getSyntaxesAsDictionary()

    @property
    def grammar(self):
        if not hasattr(self, '_grammar'):
            dataHash = {}
            dataHash['repository'] = self.buildRepository()
            dataHash['patterns'] = self.patterns if self.patterns != None else []
            setattr(self, '_grammar', PMXSyntaxNode(dataHash , self ))
        return self._grammar

    def buildRepository(self):
        repository = {}
        if self.scopeName is not None:
            syntaxes = self.syntaxes
            index = self.scopeName.find(".")
            while index != -1:
                parentScopeName = self.scopeName[0:index]
                parentSyntax = syntaxes.get(parentScopeName)
                if parentSyntax is not None and parentSyntax.repository is not None:
                    repository.update(parentSyntax.repository)
                index = self.scopeName.find(".", index + 1)
        if self.repository is not None:
            repository.update(self.repository)
        return repository

    def parse(self, string, processor = None):
        if processor:
            processor.startParsing(self.scopeName)
        stack = [[self.grammar, None]]
        for line in SPLITLINES.split(string):
            self.parseLine(stack, line, processor)
        if processor:
            processor.endParsing(self.scopeName)
    
    def parseLine(self, stack, line, processor):
        if processor:
            processor.beginLine(line)
        top, match = stack[-1]
        position = 0
        grammar = self.grammar
        
        while True:
            if top.patterns:
                pattern, pattern_match = top.match_first_son(line, position)
            else:
                pattern, pattern_match = None, None
            end_match = None
            if top.end:
                end_match = top.match_end( line, match, position )
            
            if end_match and ( not pattern_match or pattern_match.start() >= end_match.start() ):
                pattern_match = end_match
                start_pos = pattern_match.start()
                end_pos = pattern_match.end()
                if top.contentName and processor:
                    processor.closeTag(top.contentName, start_pos)
                if processor:
                    grammar.parse_captures('captures', top, pattern_match, processor)
                if processor:
                    grammar.parse_captures('endCaptures', top, pattern_match, processor)
                if top.name and processor:
                    processor.closeTag( top.name, end_pos)
                stack.pop()
                top, match = stack[-1]
            else:
                if not pattern:
                    break 
                start_pos = pattern_match.start()
                end_pos = pattern_match.end()
                if pattern.begin:
                    if pattern.name and processor:
                        processor.openTag(pattern.name, start_pos)
                    if processor:    
                        grammar.parse_captures('captures', pattern, pattern_match, processor)
                    if processor:
                        grammar.parse_captures('beginCaptures', pattern, pattern_match, processor)
                    if pattern.contentName and processor:
                        processor.openTag(pattern.contentName, end_pos)
                    top = pattern
                    match = pattern_match
                    stack.append([top, match])
                elif pattern.match:
                    if pattern.name and processor:
                        processor.openTag(pattern.name, start_pos)
                    if processor:
                        grammar.parse_captures('captures', pattern, pattern_match, processor)
                    if pattern.name and processor:
                        processor.closeTag(pattern.name, end_pos)
            position = end_pos
        if processor:
            processor.endLine(line)
        return position
    
    def folding(self, line):
        start_match = self.foldingStartMarker.search(line) if self.foldingStartMarker != None else None
        stop_match = self.foldingStopMarker.search(line) if self.foldingStopMarker != None else None
        if start_match != None and stop_match == None:
            return self.FOLDING_START
        elif stop_match != None and start_match == None:
            return self.FOLDING_STOP
        return self.FOLDING_NONE

    def __str__(self):
        return u"<PMXSyntax %s>" % self.name

    @classmethod
    def findGroup(cls, scopes):
        for scope in scopes:
            group = scope.split(".")[0]
            if group in cls.ROOT_GROUPS:
                return group
