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

from preferences import Preferences
from config import ConfigManager

class VteObjectContainer(Gtk.Box):
    def __init__(self):
        super(VteObjectContainer, self).__init__()
        self.pack_start(VteObject(),True,True,0)
        self.show_all()

class VteObject(Gtk.Box):
    def __init__(self):
        super(VteObject, self).__init__()
        ConfigManager.add_callback(self.update_ui)

        self.vte = Vte.Terminal()
        self.pack_start(self.vte,True,True,0)
        if ConfigManager.get_conf('show-scrollbar'):
            self.vscroll = Gtk.VScrollbar()
            self.vscroll.set_adjustment(self.vte.get_vadjustment())
            self.pack_end(self.vscroll,False,True,0)

        dir_conf = ConfigManager.get_conf('dir')
        if dir_conf == '$home$':
            run_dir = os.environ['HOME']
        elif dir_conf == '$pwd$':
            run_dir = os.getcwd()
        else:
            run_dir = dir_conf

        self.vte.fork_command_full(
            Vte.PtyFlags.DEFAULT, 
            run_dir,
            [ConfigManager.get_conf('shell')],
            [], 
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,
            None)
        

        self.vte.connect('button-release-event', self.on_button_release)

        self.update_ui()

    def update_ui(self):
        self.vte.set_background_saturation(ConfigManager.get_conf('transparency') / 100.0)
        self.vte.set_opacity(int((100 - ConfigManager.get_conf(('transparency'))) / 100.0 * 65535))

        self.vte.set_colors(Gdk.color_parse(ConfigManager.get_conf('color-text')),Gdk.color_parse(ConfigManager.get_conf('color-background')),[])

        self.vte.set_background_image_file(ConfigManager.get_conf('background-image'))

        if not ConfigManager.get_conf('use-default-font'):
            self.vte.set_font_from_string(ConfigManager.get_conf('font-name'))

        self.show_all()

    def on_button_release(self, widget, event):
        if event.button == 3:
            self.menu = Gtk.Menu()

            self.menu_copy = Gtk.MenuItem("Copy")
            self.menu_copy.connect("activate", self.vte.copy_clipboard)
            self.menu.append(self.menu_copy)

            self.menu_paste = Gtk.MenuItem("Paste")
            self.menu_paste.connect("activate", self.vte.paste_clipboard)
            self.menu.append(self.menu_paste)

            self.menu_select_all = Gtk.MenuItem("Select All")
            self.menu_select_all.connect("activate", self.vte.select_all)
            self.menu.append(self.menu_select_all)

            self.menu.append(Gtk.SeparatorMenuItem.new())

            self.menu_v_split = Gtk.MenuItem("Split Vertical")
            self.menu_v_split.connect("activate", self.split_axis, 'h')
            self.menu.append(self.menu_v_split)

            self.menu_h_split = Gtk.MenuItem("Split Horizontal")
            self.menu_h_split.connect("activate", self.split_axis, 'v')
            self.menu.append(self.menu_h_split)

            self.menu_close = Gtk.MenuItem("Close")
            self.menu_close.connect("activate", self.close_node)
            self.menu.append(self.menu_close)

            self.menu.append(Gtk.SeparatorMenuItem.new())

            self.menu_preferences = Gtk.MenuItem("Preferences")
            self.menu_preferences.connect("activate", self.open_preferences)
            self.menu.append(self.menu_preferences)

            self.menu_quit = Gtk.MenuItem("Quit")
            self.menu_quit.connect("activate", Gtk.main_quit)
            self.menu.append(self.menu_quit)
            
            self.menu.show_all()
                      
            self.menu.popup(None, None, None, None, event.button, event.time)
    
    def open_preferences(self, widget):
        prefs = Preferences()
        prefs.show()

    def close_node(self, widget):
        parent = self.get_parent()
        if type(parent) == VteObjectContainer:
            return

        if parent.get_child1() == self:
            sibling = parent.get_child2()
        else:
            sibling = parent.get_child1()

        ConfigManager.remove_callback(self.update_ui)
        parent.remove(sibling)
        top_level = parent.get_parent()
        if type(top_level) == VteObjectContainer:
            top_level.remove(parent)
            top_level.pack_start(sibling,True,True,0)
        else:
            if top_level.get_child1() == parent:
                top_level.remove(parent)
                top_level.pack1(sibling,True,True)
            else:
                top_level.remove(parent)
                top_level.pack2(sibling,True,True)                


    def split_axis(self, widget, axis='h'):
        parent = self.get_parent()
        if type(parent) != VteObjectContainer:
            if parent.get_child1() == self:
                mode = 1
            else:
                mode = 2
        else:
            mode = 0

        if axis == 'h':
            paned = Gtk.HPaned()
            paned.set_property('position', self.get_allocation().width / 2)
        elif axis == 'v':
            paned = Gtk.VPaned()
            paned.set_property('position', self.get_allocation().height / 2)
        parent.remove(self)
        paned.pack1(self,True,True) 
        paned.pack2(VteObject(),True,True)
        paned.show_all()
        if mode == 0:
            parent.pack_start(paned,True,True,0)
        elif mode == 1:
            parent.pack1(paned,True,True)
        else:
            parent.pack2(paned,True,True)
        parent.show_all()