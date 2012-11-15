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

from gi.repository import Gtk, Vte, GLib, Gdk
import os

from VteObject import VteObject
from config import ConfigManager

class TerminalWin(Gtk.Window):

    def __init__(self):
        super(TerminalWin, self).__init__()

        self.configmanager = ConfigManager()
        self.get_conf = self.configmanager.get_conf

        self.screen = self.get_screen()
        self.init_transparency()
        self.init_ui()
    
    def on_keypress(self, widget, event):
        if Gdk.keyval_name(event.keyval) == self.get_conf('exit-key'):
            Gtk.main_quit()

    def init_transparency(self):    
        self.set_app_paintable(True)  
        visual = self.screen.get_rgba_visual()       
        if visual != None and self.screen.is_composited():
            self.set_visual(visual)            

    def init_ui(self):
        self.connect('destroy', Gtk.main_quit)
        self.connect('key-press-event', self.on_keypress)

        self.set_decorated( self.get_conf('use-border') )
        self.set_skip_taskbar_hint( not self.get_conf('show-in-taskbar'))

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data('''*{-GtkPaned-handle-size: %i;}''' % (self.get_conf('seperator-size')))
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(self.screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

        width = self.get_conf('width') * self.screen.get_width() / 100
        height = self.get_conf('height') * self.screen.get_height() / 100
        self.resize(width, height)

        vertical_position = self.get_conf('vertical-position') * self.screen.get_height() / 100
        
        if vertical_position - (height/2) < 0:
            vertical_position = 0
        elif vertical_position + (height/2) > self.screen.get_height():
            vertical_position = self.screen.get_height() - (height/2)
        else:
            vertical_position = vertical_position - (height/2)

        horizontal_position = self.get_conf('horizontal-position') * self.screen.get_width() /100
        if horizontal_position - (width/2) < 0:
            horizontal_position = 0
        elif horizontal_position + (width/2) > self.screen.get_width():
            horizontal_position = self.screen.get_width() - (width/2)
        else:
            horizontal_position = horizontal_position - (width/2)

        self.move(horizontal_position,vertical_position)

        self.add(VteObject())

        self.show_all()

def main():
    app = TerminalWin()
    Gtk.main()
        
        
if __name__ == "__main__":    
    main()