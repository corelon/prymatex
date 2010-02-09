#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os, plistlib

PRIMATEX_BASE_PATH = os.path.abspath(os.path.curdir)
PRYMATEX_SETTINGS_FILE = os.path.join(PRIMATEX_BASE_PATH , "settings.plist")

class Settings(object):
    TEXTMATE_BUNDLES_PATH = os.path.join(PRIMATEX_BASE_PATH, 'Bundles')
    TEXTMATE_THEMES_PATH = os.path.join(PRIMATEX_BASE_PATH, 'Themes')
    
    def __init__(self):
        try:
            if os.path.exists(PRYMATEX_SETTINGS_FILE):
                config = plistlib.readPlist(PRYMATEX_SETTINGS_FILE)
            else:
                raise Exception()
        except:
            config = dict(
                          TEXTMATE_THEMES_PATHS = ["../tests/bundles/Themes", ],
                          TEXTMATE_BUNDLES_PATHS = ["../tests/bundles/Bundles", ],
                          
            )
                      
                
        for key, value in config.iteritems():
            setattr(self, key, value)
        
    def __getattr__(self, name):
        return self.__dict__.get(name, self.__class__.__dict__.get(name)) 
    
    def __setattr__(self, name, value):
        self.__dict__[name] = value
    
    def save(self):
        plistlib.writePlist(self.__dict__, PRYMATEX_SETTINGS_FILE)
    
    def __str__(self):
        return str(self.__dict__)
        
settings = Settings()

if __name__ == '__main__':
    print settings
    #Ponemos algo en settings, efecto configuracion de usuario
    settings.save()