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

from gi.repository import Gtk
import os

from config import ConfigManager

class Preferences():

    def __init__(self):
        self.configmanager = ConfigManager()
        self.get_conf = self.configmanager.get_conf

        self.init_ui()

    def init_ui(self):
        builder = Gtk.Builder()
        builder.add_from_file("ui/preferences.ui")

        self.window = builder.get_object("window1")
        self.window.connect('destroy', Gtk.main_quit)

    def show(self):
        self.window.show_all()