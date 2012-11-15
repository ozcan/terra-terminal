#!/usr/bin/python
import ConfigParser
import os
class ConfigManager():

    def __init__(self):
        self.config = ConfigParser.SafeConfigParser({'bar': 'Life', 'baz': 'hard'})
        self.cfg_file = "main.cfg"
        if not os.path.isfile(self.cfg_file):
            self.config.read(self.cfg_file)
            
            self.config_data = {
                'vertical-aligment': 0,
                'horizontal-aligment': 0,
                'height': 20,
                'width': 100,

            }

    def read_conf(self, key, default):
        print self.config.get('default', key)
        
    def get_conf(self, key):
        if self.config_data.has_key(key):
            return self.config_data[key]
        print "Debug: %s key not found in config data." % (key)
        return None

    def set_conf(self, key, value):
        if self.config_data.has_key(key):
            self.config_data[key] = value
            return True
        print "Debug: %s key not found in config data." % (key)
        return None
       

a = ConfigManager()
print a.read_conf('width', 200)