#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Command's module
        content, name, scope, keyEquivalent, tabTrigger
'''

from pprint import pprint

COMMANDS = {}

class Command(object):
    def __init__(self, hash, name_space):
        #pprint(hash)
        self.name_space = name_space
        COMMANDS.setdefault(self.name_space, {})
        #Todo lo que diga scope es en que scope esta, puede ser mas de uno
        if 'scope' in hash:
            scopes = hash['scope'].split(', ')
            for scope in scopes:
                COMMANDS[self.name_space][scope] = self 
        self.content = hash.get('content')
        self.name = hash.get('name')
        self.keyEquivalent = hash.get('keyEquivalent')
        self.tabTrigger = hash.get('tabTrigger')