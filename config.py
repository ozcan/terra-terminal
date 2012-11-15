#!/usr/bin/python
# -*- coding: utf-8; -*-
"""
Copyright (C) 2012 - Ozcan ESEN <ozcanesen~gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>

"""

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