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

from gi.repository import Gtk, Vte, GLib, Gdk, GdkPixbuf
import os

from VteObject import VteObject, VteObjectContainer
from config import ConfigManager

class TerminalWin(Gtk.Window):

    def __init__(self):
        super(TerminalWin, self).__init__()

        self.builder = Gtk.Builder()
        self.builder.add_from_file('ui/main.ui')

        ConfigManager.add_callback(self.update_ui)
        self.get_conf = ConfigManager.get_conf

        self.screen = self.get_screen()

        self.init_transparency()
        self.init_ui()
        self.update_ui()
        self.show()
        self.add_page()

    def init_ui(self):
        self.main_container = self.builder.get_object('main_container')
        self.main_container.unparent()

        self.logo = self.builder.get_object('logo')
        self.logo_buffer = GdkPixbuf.Pixbuf.new_from_file_at_size('terminal.svg', 32, 32)
        self.logo.set_from_pixbuf(self.logo_buffer)

        self.notebook = self.builder.get_object('notebook')
        self.buttonbox = self.builder.get_object('buttonbox')
        self.radio_group_leader = Gtk.RadioButton()
        self.buttonbox.pack_start(self.radio_group_leader,False,False,0)
        self.radio_group_leader.hide()
        self.radio_button_list = []
        self.new_page_button = self.builder.get_object('new_page_button')
        self.new_page_button.connect('clicked', lambda w: self.add_page())

        self.connect('destroy', Gtk.main_quit)
        self.connect('key-press-event', self.on_keypress)

        self.add(self.main_container)


    def add_page(self):
        self.notebook.append_page(VteObjectContainer(), None)
        self.notebook.set_current_page(-1)

        new_button = Gtk.RadioButton.new_with_label_from_widget(self.radio_group_leader, "Terminal " + str(self.notebook.get_current_page()+1))
        new_button.set_property('draw-indicator', False)
        new_button.set_active(True)
        new_button.show()
        new_button.connect('toggled', self.change_page)
        self.radio_button_list.append(new_button)
        self.buttonbox.pack_start(new_button,False,True,0)

    def change_page(self, button):
        if button.get_active() == False:
            return

        if not button in self.radio_button_list:
            return

        for i in xrange(len(self.radio_button_list)):
            if self.radio_button_list[i] == button:
                self.notebook.set_current_page(i)

    def update_ui(self):

        self.set_decorated( self.get_conf('use-border') )
        self.set_skip_taskbar_hint( self.get_conf('show-in-taskbar'))

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

    def on_keypress(self, widget, event):
        if Gdk.keyval_name(event.keyval) == self.get_conf('exit-key'):
            Gtk.main_quit()

    def init_transparency(self):    
        self.set_app_paintable(True)  
        visual = self.screen.get_rgba_visual()       
        if visual != None and self.screen.is_composited():
            self.set_visual(visual)            

def main():
    app = TerminalWin()
    Gtk.main()
        
        
if __name__ == "__main__":    
    main()