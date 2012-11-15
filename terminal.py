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

class TerminalWin(Gtk.Window):

    def __init__(self):
        super(TerminalWin, self).__init__()
        self.transparency_setup()
        self.init_ui()

    def toggle_window(self):
        # this will used by global hotkey later
        if self.get_visible():
            self.set_visible(False)
        else:
            self.set_visible(True)
    
    def keypress(self, widget, event):
        if Gdk.keyval_name(event.keyval) == "Escape":
            #self.hide()
            Gtk.main_quit()

    def transparency_setup(self):    
        self.set_app_paintable(True)  
        screen = self.get_screen()
        visual = screen.get_rgba_visual()       
        if visual != None and screen.is_composited():
            self.set_visual(visual)            

    def init_ui(self):
        # set border type and title
        self.set_title("Terminal Emulator")
        self.set_decorated(False)
        # disable taskbar and alt+tab icons
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)

        screen = Gdk.Screen.get_default()
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data("*{-GtkPaned-handle-size: 3;}")
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
        # set coordinates
        self.move(0,0)
        self.resize(self.get_screen().get_width(), 300)
        # init widgets
        #self.add(self.vpaned)
        self.mainpanel = Gtk.VBox(False, 0)
        self.mainpanel.pack_start(VteObject(),True,True,0)
        #self.bottommenu = Gtk.HBox(False,0)
        #self.bottommenu.set_size_request(0,20)
        #self.mini_logo = Gtk.Image()
        #self.mini_logo.set_from_file('terminal.svg')
        #self.bottommenu.pack_start(self.mini_logo,False,False,0)
        #self.mainpanel.pack_end(self.bottommenu, False,True,0)
        self.add(self.mainpanel)
        # connect signals and show window
        # self.connect("draw", self.on_draw)
        self.connect("destroy", Gtk.main_quit)
        self.connect("key-press-event", self.keypress)
        self.show_all()




def main():
    app = TerminalWin()
    Gtk.main()
        
        
if __name__ == "__main__":    
    main()