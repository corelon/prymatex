#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import QObject, pyqtWrapperType
import re
from prymatex.core.event import PMXEventSender
from prymatex.core.config import SettingsGroup
from PyQt4.QtGui import qApp
METHOD_RE = re.compile('(?P<name>[\w\d_]+)(:?\((?P<args>.*)\))?', re.IGNORECASE)

class InvalidEventSignature(Exception):
    pass

settings = qApp.instance().settings

EVENT_CLASSES = {}

class PMXOptions(object):
    def __init__(self, options):
        self.settings = settings.getGroup(getattr(options, 'settings', ''))
        self.events = getattr(options, 'events', None)

class PMXObjectBase(pyqtWrapperType):
    def __new__(cls, name, bases, attrs):
        module = attrs.pop('__module__')
        new_class = super(PMXObjectBase, cls).__new__(cls, name, bases, { '__module__': module })
        opts = PMXOptions(attrs.get('Meta', None))
        new_class.add_to_class('_meta', opts)
        for name, attr in attrs.iteritems():
            new_class.add_to_class(name, attr)
        return new_class

    def add_to_class(cls, name, value): #@NoSelf
        if hasattr(value, 'contributeToClass'):
            value.contributeToClass(cls, name)
        else:
            setattr(cls, name, value)

from logging import getLogger

class PMXObject(QObject):
    __metaclass__ = PMXObjectBase

    def configure(self):
        self._meta.settings.addListener(self)
        self._meta.settings.configure(self)
    
    def declareEvent(self, signature):
        global EVENT_CLASSES
        match = METHOD_RE.match(signature)
        if not match:
                raise InvalidEventSignature(signature)
        name, args = match.group('name'), match.group('args')
        event_class = EVENT_CLASSES.setdefault(name, PMXEventSender.eventFactory(name))
        
        sender = PMXEventSender(event_class = event_class, source = self)
        setattr(self, name, sender)
        return sender

    def connectEventsByName(self):
        raise NotImplementedError("Not implemented error")
    
    @property
    def mainWindow(self):
        main = self
        while main.parent() != None:
            main = main.parent()
        return main
       
    mainwindow = mainWindow # TODO: Remove
    
    
    # Logging 
    _logger = None
    @property
    def logger(self):
        '''
        Per class logger, logger instances are named after
        classes, ie: prymatex.gui.mainwindow.PMXMainWindow 
        '''
        if self._logger is None:
            t = type(self)
            loggername = '.'.join([t.__module__, t.__name__])
            self.__class__._logger = getLogger(loggername)
        return self._logger
    
    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg)
    
    def info(self, msg, *args, **kwargs):
        self.logger.info(msg)
    
    def warn(self, msg, *args, **kwargs):
        self.logger.warn(msg)
    
    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg)