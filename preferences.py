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

from gi.repository import Gtk, Gdk
import os

from config import ConfigManager

class Preferences():

    def __init__(self):
        self.init_ui()

    def init_ui(self):
        builder = Gtk.Builder()
        builder.add_from_file('ui/preferences.ui')

        self.window = builder.get_object('preferences_window')

        self.window.btn_cancel = builder.get_object('btn_cancel')
        self.window.btn_cancel.connect('clicked', self.on_cancel_clicked)

        self.window.btn_apply = builder.get_object('btn_apply')
        self.window.btn_apply.connect('clicked', self.on_apply_clicked)

        self.window.btn_ok = builder.get_object('btn_ok')
        self.window.btn_ok.connect('clicked', self.on_ok_clicked)

        self.window.adj_seperator = builder.get_object('adjustment_seperator')
        self.window.adj_seperator.set_value(int(ConfigManager.get_conf('seperator-size')) * 1.0)

        self.window.adj_width = builder.get_object('adjustment_width')
        self.window.adj_width.set_value(int(ConfigManager.get_conf('width')) * 1.0)

        self.window.adj_height = builder.get_object('adjustment_height')
        self.window.adj_height.set_value(int(ConfigManager.get_conf('height')) * 1.0)

        self.window.adj_transparency = builder.get_object('adjustment_transparency')
        self.window.adj_transparency.set_value(int(ConfigManager.get_conf('transparency')) * 1.0)

        self.v_alig = builder.get_object('v_alig')
        self.v_alig.set_active(int(ConfigManager.get_conf('vertical-position')) / 50)

        self.h_alig = builder.get_object('h_alig')
        self.h_alig.set_active(int(ConfigManager.get_conf('horizontal-position')) / 50)

        self.chk_hide_from_taskbar = builder.get_object('chk_hide_from_taskbar')
        self.chk_hide_from_taskbar.set_active(ConfigManager.get_conf('skip-taskbar'))

        self.chk_close_with_escape = builder.get_object('chk_close_with_escape')
        self.chk_close_with_escape.set_active(ConfigManager.get_conf('close-with-escape'))

        self.chk_allow_fullscreen = builder.get_object('chk_allow_fullscreen')
        self.chk_allow_fullscreen.set_active(ConfigManager.get_conf('allow-fullscreen'))

        self.chk_use_border = builder.get_object('chk_use_border')
        self.chk_use_border.set_active(ConfigManager.get_conf('use-border'))

        self.color_text = builder.get_object('color_text')
        self.color_text.set_color(Gdk.color_parse(ConfigManager.get_conf('color-text')))

        self.color_background = builder.get_object('color_background')
        self.color_background.set_color(Gdk.color_parse(ConfigManager.get_conf('color-background')))

        self.entry_shell = builder.get_object('entry_shell')
        self.entry_shell.set_text(ConfigManager.get_conf('shell'))

        self.dir_custom = builder.get_object('dir_custom')

        self.radio_home = builder.get_object('radio_home')
        self.radio_pwd = builder.get_object('radio_pwd')
        self.radio_dir_custom = builder.get_object('radio_dir_custom')
        self.radio_dir_custom.connect('toggled', lambda w: self.dir_custom.set_sensitive(self.radio_dir_custom.get_active()))

        dir_conf = ConfigManager.get_conf('dir')
        if dir_conf == '$home$':
            self.radio_home.set_active(True)
        elif dir_conf == '$pwd$':
            self.radio_pwd.set_active(True)
        else:
            self.radio_dir_custom.set_active(True)
            self.dir_custom.set_text(dir_conf)
            self.dir_custom.set_sensitive(True)

        self.background_image = builder.get_object('background_image')
        self.background_image.set_filename(ConfigManager.get_conf('background-image'))

        self.clear_background_image = builder.get_object('clear_background_image')
        self.clear_background_image.connect('clicked', lambda w: self.background_image.unselect_all())

        self.font_name = builder.get_object('font_name')
        self.font_name.set_font_name(ConfigManager.get_conf('font-name'))

        self.chk_use_system_font = builder.get_object('chk_use_system_font')
        self.chk_use_system_font.connect('toggled', lambda w: self.font_name.set_sensitive(not self.chk_use_system_font.get_active()))
        self.chk_use_system_font.set_active(ConfigManager.get_conf('use-default-font'))
    def show(self):
        self.window.show_all()

    def on_apply_clicked(self, widget):
        ConfigManager.set_conf('seperator-size',int(self.window.adj_seperator.get_value()))

        ConfigManager.set_conf('width',int(self.window.adj_width.get_value()))

        ConfigManager.set_conf('height',int(self.window.adj_height.get_value()))

        ConfigManager.set_conf('transparency',int(self.window.adj_transparency.get_value()))

        ConfigManager.set_conf('vertical-position', self.v_alig.get_active() * 50)

        ConfigManager.set_conf('horizontal-position', self.h_alig.get_active() * 50)

        ConfigManager.set_conf('skip-taskbar', self.chk_hide_from_taskbar.get_active())

        ConfigManager.set_conf('close-with-escape', self.chk_close_with_escape.get_active())

        ConfigManager.set_conf('allow-fullscreen', self.chk_allow_fullscreen.get_active())

        ConfigManager.set_conf('use-border', self.chk_use_border.get_active())

        ConfigManager.set_conf('color-text', self.color_text.get_color().to_string())

        ConfigManager.set_conf('color-background', self.color_background.get_color().to_string())

        ConfigManager.set_conf('shell', self.entry_shell.get_text())

        if self.radio_home.get_active():
            ConfigManager.set_conf('dir', '$home$')
        elif self.radio_pwd.get_active():
            ConfigManager.set_conf('dir', '$pwd$')
        else:
            ConfigManager.set_conf('dir', self.dir_custom.get_text())

        ConfigManager.set_conf('background-image', self.background_image.get_filename())

        ConfigManager.set_conf('use-default-font', self.chk_use_system_font.get_active())

        ConfigManager.set_conf('font-name', self.font_name.get_font_name())

        ConfigManager.save_config()
        ConfigManager.callback()

    def on_ok_clicked(self, widget):
        self.on_apply_clicked(self.window.btn_ok)
        self.window.hide()

    def on_cancel_clicked(self, widget):
        self.window.hide()
