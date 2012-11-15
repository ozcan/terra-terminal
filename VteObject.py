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

class VteObject(Vte.Terminal):
    def __init__(self, *args, **kwds):
        super(VteObject, self).__init__(*args, **kwds)
        self.set_background_saturation(20 / 100.0)
        self.set_opacity(int((100 - 20) / 100.0 * 65535))
        self.fork_command_full(Vte.PtyFlags.DEFAULT, os.environ['HOME'],[os.environ['SHELL']],[], GLib.SpawnFlags.DO_NOT_REAP_CHILD,None,None)
        self.connect("button-release-event", lambda x,y: self.button_press(y))

    def button_press(self, event):
        if event.button == 3:
            self.menu = Gtk.Menu()
            self.menu_copy = Gtk.MenuItem("Copy")
            self.menu_paste = Gtk.MenuItem("Paste")
            self.menu_select_all = Gtk.MenuItem("Select All")
            self.menu_v_split = Gtk.MenuItem("Split Vertical")
            self.menu_h_split = Gtk.MenuItem("Split Horizontal")
            self.menu_close = Gtk.MenuItem("Close")
            self.menu_quit = Gtk.MenuItem("Quit")
            self.menu.append(self.menu_copy)
            self.menu.append(self.menu_paste)
            self.menu.append(self.menu_select_all)
            self.menu.append(Gtk.SeparatorMenuItem.new())
            self.menu.append(self.menu_v_split)
            self.menu.append(self.menu_h_split)
            self.menu.append(self.menu_close)
            self.menu.append(Gtk.SeparatorMenuItem.new())
            self.menu.append(self.menu_quit)
            self.menu.show_all()
            self.menu_v_split.connect("activate", lambda x: self.split_axis('h'))
            self.menu_h_split.connect("activate", lambda x: self.split_axis('v'))
            self.menu_close.connect("activate", lambda x: self.close_node())
            self.menu_quit.connect("activate", lambda x: Gtk.main_quit())
            self.menu_copy.connect("activate", lambda x: self.copy_clipboard())
            self.menu_paste.connect("activate", lambda x: self.paste_clipboard())
            self.menu_select_all.connect("activate", lambda x: self.select_all())

            self.menu.popup(None, None, None, None, event.button, event.time)

    def close_node(self):
        parent = self.get_parent()
        if type(parent) != Gtk.HPaned and type(parent) != Gtk.VPaned:
            return

        if parent.get_child1() == self:
            sibling = parent.get_child2()
        else:
            sibling = parent.get_child1()

        parent.remove(sibling)
        top_level = parent.get_parent()
        if type(top_level) == TerminalWin:
            top_level.remove(parent)
            top_level.add(sibling)
        else:
            if top_level.get_child1() == parent:
                top_level.remove(parent)
                top_level.pack1(sibling,True,True)
            else:
                top_level.remove(parent)
                top_level.pack2(sibling,True,True)                


    def split_axis(self, axis='h'):
        parent = self.get_parent()
        if type(parent) == Gtk.HPaned or type(parent) == Gtk.VPaned:
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
            parent.add(paned)
        elif mode == 1:
            parent.pack1(paned,True,True)
        else:
            parent.pack2(paned,True,True)
        parent.show_all()