#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import os, plistlib

def get_prymatex_base_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def get_prymatex_user_path():
    path = os.path.join(os.path.expanduser("~"), ".prymatex")
    if not os.path.exists(path):
        os.makedirs(path)
    return path

PMX_BASE_PATH = get_prymatex_base_path()
PMX_USER_PATH = get_prymatex_user_path()
PMX_SETTINGS_FILE = os.path.join(PMX_USER_PATH , "settings.plist")

class SettingsNode(object):
    def __init__(self, hash = {}):
        self.__dict__['__wrapped_values'] = dict()
        self.__dict__['__wrapped_defaults'] = dict()
        self.__dict__['__listeners'] = []
        for key, value in hash.iteritems():
            setattr(self, key, value)
    
    def __setattr__(self, name, value):
        if isinstance(value, dict) and value.has_key('type') and value['type'] == "SettingsNode":
            value = SettingsNode(value)
        self.__dict__['__wrapped_values'][name] = value
        for listener in self.__dict__['__listeners']:
            setattr(listener, name, value)
    
    def __getattr__(self, name, default = None): 
        try:
            return self.get_value_for(name)
        except KeyError:
            if default == None:
                setattr(self, name, SettingsNode())
                return self.__dict__['__wrapped_values'][name]
        return default
    
    def __getitem__(self, name):
        return self.__dict__['__wrapped_values'][name]
    
    def __setitem__(self, name, value):
        self.__dict__['__wrapped_defaults'][name] = value
    
    def get_value_for(self, name):
        if self.__dict__['__wrapped_values'].has_key(name):
            return self.__dict__['__wrapped_values'][name]
        elif self.__dict__['__wrapped_defaults'].has_key(name):
            return self.__dict__['__wrapped_defaults'][name]
        raise KeyError()
    
    def add_listener(self, listener):
        self.__dict__['__listeners'].append(listener)
    
    def to_python(self):
        ret = {'type': self.__class__.__name__}
        for k, v in self.__dict__['__wrapped_values'].iteritems():
            if hasattr(v, 'to_python'):
                ret[k] = v.to_python()
            else:
                ret[k] = v
        return ret
    
class Settings(SettingsNode):
    '''
    Configuración gerarquica basada en diccionarios.
    '''
    PMX_BUNDLES_PATH = os.path.join(PMX_BASE_PATH, 'share', 'Bundles')
    PMX_THEMES_PATH = os.path.join(PMX_BASE_PATH, 'share', 'Themes')
    PMX_SUPPORT_PATH = os.path.join(PMX_BASE_PATH, 'share', 'Support')
    
    def __init__(self, parent = None, **defaults):
        if os.path.exists(PMX_SETTINGS_FILE):
            wrapped_dict = plistlib.readPlist(PMX_SETTINGS_FILE)
        else:
            wrapped_dict = {}
        super(Settings, self).__init__(wrapped_dict)
        
    def save(self):
        obj = self.to_python()
        plistlib.writePlist(obj, PMX_SETTINGS_FILE)

settings = Settings()

class Setting(object):
    def __init__(self, default = None):
        self.__value = None
        self.__default = default
    
    def get_value(self):
        return self.__value or self.__default
    
    def set_value(self, value):
        self.__value = value
    
    value = property(get_value, set_value)
    
    def contribute_to_class(self, cls, name):
        self.name = name
        try:
            self.__value = cls._meta.settings[self.name]
        except KeyError:
            cls._meta.settings[self.name] = self.__default
        
        self.fget = getattr(cls, self.name, None)
        self.fset = getattr(cls, "set%s" % self.name.title(), None)
        setattr(cls, self.name, self)
        
    def __get__(self, instance, instance_type = None):
        if instance != None:
            return self.value
        elif self.fget != None:
            return self.fget(instance)
    
    def __set__(self, instance, value):
        if instance != None:
            self.__value = value
        if self.fset != None:
            self.fset(instance, self.__value)

if __name__ == "__main__":    
    class PMXOptions(object):
        def __init__(self, options=None):
            self.settings = settings
            space = getattr(options, 'settings', None)
            if space != None:
                spaces = space.split('.')
                for s in spaces:
                    self.settings = getattr(self.settings, s)
            self.events = getattr(options, 'events', None)
    
    class PersonaBase(type):
        def __new__(cls, name, bases, attrs):
            module = attrs.pop('__module__')
            new_class = super(PersonaBase, cls).__new__(cls, name, bases, { '__module__': module })
            opts = PMXOptions(attrs.get('Meta', None))
            new_class.add_to_class('_meta', opts)
            for name, attr in attrs.iteritems():
                new_class.add_to_class(name, attr)
            return new_class

        def add_to_class(cls, name, value):
            if hasattr(value, 'contribute_to_class'):
                value.contribute_to_class(cls, name)
            else:
                setattr(cls, name, value)
        
    class Persona():
        __metaclass__ = PersonaBase
        def __init__(self, nombre):
            self.nombre = nombre
            self.configure()
        
        def configure(self):
            self._meta.settings.add_listener(self)
        
    class Empleado(Persona):
        cargo = Setting(default = 'Programador Jr.')
        sueldo = Setting(default = 100)
        
        def __init__(self, nombre):
            super(Empleado, self).__init__(nombre)

        class Meta(object):
            events = ('uno', 'dos', )
            settings = 'empleado'
            
    class Jefe(Empleado):
        sueldo = Setting(default = 200)
        
        def __init__(self, nombre):
            super(Jefe, self).__init__(nombre)
            
        class Meta(object):
            events = ('uno', 'dos', )
            settings = 'empleado.jefe'
    
    j = Jefe("Caho")
    e = Empleado("Caho")
    settings.empleado.jefe.cargo = "Cachin comodin"
    settings.empleado.sueldo = 4000
    settings.empleado.jefe.sueldo = 5000
    print e.sueldo, j.sueldo
    print e.cargo, j.cargo