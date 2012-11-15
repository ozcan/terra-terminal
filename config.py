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

class ConfigManager():

    def __init__(self):
        self.config = ConfigParser.SafeConfigParser(
            {
            'seperator-size': '10',
            'exit-key': 'Escape',
            'use-border': 'True',
            'show-in-taskbar': 'True',
            'height': '40',
            'width': '50',
            'horizontal-position': '0',
            'vertical-position': '0'
            })
        self.cfg_file = 'main.cfg'
        self.namespace = 'default'
        self.config.read(self.cfg_file)

    def get_conf(self, key):
        try:
            value = self.config.get(self.namespace, key)
        except ConfigParser.NoOptionError:
            print "[DEBUG] No option '%s' found in file '%s'" % (key, self.namespace)
            return None

        try:
            return int(value)
        except ValueError:
            if value == 'True':
                return True
            elif value == 'False':
                return False
            else:
                return value


