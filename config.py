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


class  ConfigManager():
    config = ConfigParser.SafeConfigParser(
        {
        'seperator-size': '2',
        'close-with-escape': 'True',
        'use-border': 'False',
        'skip-taskbar': 'False',
        'skip-pager': 'False',
        'height': '40',
        'width': '100',
        'horizontal-position': '50',
        'vertical-position': '0',
        'allow-fullscreen': 'True',
        'color-text': '#ffffffffffff',
        'color-background': '#000000000000',
        'transparency': '50',
        'shell': os.environ['SHELL'],
        'dir': '$home$',
        'background-image': '',
        'use-default-font': 'True',
        'font-name': 'Monospace 10',
        'show-scrollbar': 'True'
        })

    cfg_dir = '/.config/terra/'
    cfg_file = 'main.cfg'
    cfg_full_path = os.environ['HOME'] + cfg_dir + cfg_file

    namespace = 'DEFAULT'
    config.read(cfg_full_path)

    callback_list = []

    @staticmethod
    def get_conf(key):
        try:
            value = ConfigManager.config.get(ConfigManager.namespace, key)
        except ConfigParser.Error:
            print ("[DEBUG] No option '%s' found in namespace '%s'." %
                    (key, ConfigManager.namespace))
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

    @staticmethod
    def set_conf(key, value):
        try:
            ConfigManager.config.set(ConfigManager.namespace, key, str(value))
        except ConfigParser.Error:
            print ("[DEBUG] No option '%s' found in namespace '%s'." %
                    (key, ConfigManager.namespace))
            return

    @staticmethod
    def save_config():
        if not os.path.exists(os.environ['HOME'] + ConfigManager.cfg_dir):
            os.mkdir(os.environ['HOME'] + ConfigManager.cfg_dir)

        with open(ConfigManager.cfg_full_path, 'wb') as configfile:
            ConfigManager.config.write(configfile)

        ConfigManager.config.read(ConfigManager.cfg_file)

    @staticmethod
    def add_callback(method):
        if not method in ConfigManager.callback_list:
            ConfigManager.callback_list.append(method)

    @staticmethod
    def remove_callback(method):
        if method in ConfigManager.callback_list:
            for i in xrange(len(ConfigManager.callback_list)):
                if ConfigManager.callback_list[i] == method:
                    del ConfigManager.callback_list[i]
                    return

    @staticmethod
    def callback():
        for method in ConfigManager.callback_list:
            method()
