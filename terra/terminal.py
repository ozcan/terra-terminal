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

from gi.repository import Gtk, Vte, GLib, Gdk, GdkPixbuf, GObject
from globalkeybinding import GlobalKeyBinding

from VteObject import VteObjectContainer
from config import ConfigManager

import os

class TerminalWin(Gtk.Window):

    def __init__(self):
        super(TerminalWin, self).__init__()

        self.keybinding = None
        self.builder = Gtk.Builder()
        self.builder.add_from_file(ConfigManager.data_dir + 'ui/main.ui')

        ConfigManager.add_callback(self.update_ui)
        ConfigManager.show_hide_callback = self.show_hide

        self.screen = self.get_screen()
        self.losefocus_time = 0
        self.init_transparency()
        self.init_ui()
        self.add_page()
        self.update_ui()
        

        if ConfigManager.get_conf('hide-on-start'):
            self.hide()

    def init_ui(self):
        self.set_title('Terra Terminal Emulator')
        self.is_fullscreen = False

        self.resizer = self.builder.get_object('resizer')
        self.resizer.unparent()
        self.resizer.connect('motion-notify-event', self.on_resize)
        self.resizer.connect('button-release-event', self.update_resizer)

        self.logo = self.builder.get_object('logo')
        self.logo_buffer = GdkPixbuf.Pixbuf.new_from_file_at_size(ConfigManager.data_dir  + 'image/terra.svg', 32, 32)
        self.logo.set_from_pixbuf(self.logo_buffer)

        self.set_icon(self.logo_buffer)

        self.notebook = self.builder.get_object('notebook')
        self.notebook_page_counter = 0
        self.notebook.set_name('notebook')
        self.buttonbox = self.builder.get_object('buttonbox')
        self.radio_group_leader = Gtk.RadioButton()
        self.buttonbox.pack_start(self.radio_group_leader, False, False, 0)
        self.radio_group_leader.set_no_show_all(True)

        self.new_page = self.builder.get_object('btn_new_page')
        self.new_page.connect('clicked', lambda w: self.add_page())

        self.btn_fullscreen = self.builder.get_object('btn_fullscreen')
        self.btn_fullscreen.connect('clicked', lambda w: self.toggle_fullscreen())

        self.connect('destroy', lambda w: self.quit())
        self.connect('key-press-event', self.on_keypress)
        #self.connect('focus-out-event', self.on_losefocus)

        self.add(self.resizer)

    def on_resize(self, widget, event):
        if Gdk.ModifierType.BUTTON1_MASK & event.get_state() != 0:
            mouse_y = event.device.get_position()[2]
            new_height = mouse_y - self.get_position()[1]
            if new_height > 0:
                self.resize(self.get_allocation().width, new_height)
                self.show()

    def update_resizer(self, widget, event):
        self.resizer.set_position(self.get_allocation().height)

        if not self.is_fullscreen:
            new_percent = int((self.get_allocation().height * 1.0) / self.screen.get_height() * 100.0)
            ConfigManager.set_conf('height', str(new_percent))
            ConfigManager.save_config()

    # not working
    def on_losefocus(self, window, event):
        if ConfigManager.get_conf('losefocus-hiding') and not ConfigManager.disable_losefocus_temporary:
            self.hide()

    def add_page(self):
        self.notebook.append_page(VteObjectContainer(), None)
        self.notebook.set_current_page(-1)
        self.notebook.get_nth_page(self.notebook.get_current_page()).active_terminal.vte.grab_focus()
        self.notebook_page_counter += 1
        new_button = Gtk.RadioButton.new_with_label_from_widget(self.radio_group_leader, "Terminal " + str(self.notebook_page_counter))

        new_button.set_property('draw-indicator', False)
        new_button.set_active(True)
        new_button.show()
        new_button.connect('toggled', self.change_page)
        new_button.connect('button-release-event', self.page_button_mouse_event)
        self.buttonbox.pack_start(new_button, False, True, 0)

    def change_page(self, button):
        if button.get_active() == False:
            return

        page_no = 0
        for i in self.buttonbox:
            if i != self.radio_group_leader:
                if i == button:
                    self.notebook.set_current_page(page_no)
                    self.notebook.get_nth_page(page_no).active_terminal.vte.grab_focus()
                    return
                page_no = page_no + 1

    def page_button_mouse_event(self, button, event):
        if event.button != 3:
            return

        self.menu = self.builder.get_object('page_button_menu')
        self.menu.connect('deactivate', lambda w: setattr(ConfigManager, 'disable_losefocus_temporary', False))

        self.menu_close = self.builder.get_object('menu_close')
        self.menu_rename = self.builder.get_object('menu_rename')

        try:
            self.menu_rename.disconnect(self.menu_rename_signal)
            self.menu_close.disconnect(self.menu_close_signal)

            self.menu_close_signal = self.menu_close.connect('activate', self.page_close, button)
            self.menu_rename_signal = self.menu_rename.connect('activate', self.page_rename, button)
        except:
            self.menu_close_signal = self.menu_close.connect('activate', self.page_close, button)
            self.menu_rename_signal = self.menu_rename.connect('activate', self.page_rename, button)

        self.menu.show_all()

        ConfigManager.disable_losefocus_temporary = True
        self.menu.popup(None, None, None, None, event.button, event.time)

    def page_rename(self, menu, sender):
        RenameDialog(sender)

    def page_close(self, menu, sender):
        button_count = 0
        for i in self.buttonbox:
            button_count = button_count + 1

        if button_count <= 2:
            return

        page_no = 0
        for i in self.buttonbox:
            if i != self.radio_group_leader:
                if i == sender:
                    self.notebook.remove_page(page_no)
                    self.buttonbox.remove(i)
                    for j in self.buttonbox:
                        last_button = j
                    last_button.set_active(True)
                    return
                page_no = page_no + 1

    def update_ui(self):

        self.set_decorated(ConfigManager.get_conf('use-border'))
        self.set_skip_taskbar_hint(ConfigManager.get_conf('skip-taskbar'))

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data('''#notebook GtkPaned {-GtkPaned-handle-size: %i;}''' % (ConfigManager.get_conf('seperator-size')))
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(self.screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

        if self.is_fullscreen:
            self.fullscreen()
            width = self.screen.get_width()
            height = self.screen.get_height()
        else:
            self.unfullscreen()
            width = ConfigManager.get_conf('width') * self.screen.get_width() / 100
            height = ConfigManager.get_conf('height') * self.screen.get_height() / 100
            self.resize(width, height)

        vertical_position = ConfigManager.get_conf('vertical-position') * self.screen.get_height() / 100
        if vertical_position - (height / 2) < 0:
            vertical_position = 0
        elif vertical_position + (height / 2) > self.screen.get_height():
            vertical_position = self.screen.get_height() - (height / 2)
        else:
            vertical_position = vertical_position - (height / 2)

        horizontal_position = ConfigManager.get_conf('horizontal-position') * self.screen.get_width() / 100
        if horizontal_position - (width / 2) < 0:
            horizontal_position = 0
        elif horizontal_position + (width / 2) > self.screen.get_width():
            horizontal_position = self.screen.get_width() - (width / 2)
        else:
            horizontal_position = horizontal_position - (width / 2)

        self.move(horizontal_position, vertical_position)
        self.show_all()

    def on_keypress(self, widget, event):
        if ConfigManager.key_event_compare('quit-key', event):
            Gtk.main_quit()
            return True

        if ConfigManager.key_event_compare('select-all-key', event):
            self.notebook.get_nth_page(self.notebook.get_current_page()).active_terminal.vte.select_all()
            return True

        if ConfigManager.key_event_compare('copy-key', event):
            self.notebook.get_nth_page(self.notebook.get_current_page()).active_terminal.vte.copy_clipboard()
            return True

        if ConfigManager.key_event_compare('paste-key', event):
            self.notebook.get_nth_page(self.notebook.get_current_page()).active_terminal.vte.paste_clipboard()
            return True

        if ConfigManager.key_event_compare('split-v-key', event):
            self.notebook.get_nth_page(self.notebook.get_current_page()).active_terminal.split_axis(None, 'v')
            return True

        if ConfigManager.key_event_compare('split-h-key', event):
            self.notebook.get_nth_page(self.notebook.get_current_page()).active_terminal.split_axis(None, 'h')
            return True

        if ConfigManager.key_event_compare('close-node-key', event):
            self.notebook.get_nth_page(self.notebook.get_current_page()).active_terminal.close_node(None)
            return True

        if ConfigManager.key_event_compare('fullscreen-key', event):
            self.toggle_fullscreen()
            return True

        if ConfigManager.key_event_compare('new-page-key', event):
            self.add_page()
            return True

        if ConfigManager.key_event_compare('rename-page-key', event):
            for button in self.buttonbox:
                if button != self.radio_group_leader and button.get_active():
                    self.page_rename(None, button)
                    return True

        if ConfigManager.key_event_compare('close-page-key', event):
            for button in self.buttonbox:
                if button != self.radio_group_leader and button.get_active():
                    self.page_close(None, button)
                    return True

        if ConfigManager.key_event_compare('next-page-key', event):
            page_button_list = []
            for button in self.buttonbox:
                if button != self.radio_group_leader:
                    page_button_list.append(button)

            for i in range(len(page_button_list)):
                if (page_button_list[i].get_active() == True):
                    if (i + 1 < len(page_button_list)):
                        page_button_list[i+1].set_active(True)
                    else:
                        page_button_list[0].set_active(True)
                    return True


        if ConfigManager.key_event_compare('prev-page-key', event):
            page_button_list = []
            for button in self.buttonbox:
                if button != self.radio_group_leader:
                    page_button_list.append(button)

            for i in range(len(page_button_list)):
                if page_button_list[i].get_active():
                    if i > 0:
                        page_button_list[i-1].set_active(True)
                    else:
                        page_button_list[-1].set_active(True)
                    return True

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        self.update_ui()

    def init_transparency(self):
        self.set_app_paintable(True)
        visual = self.screen.get_rgba_visual()
        if visual != None and self.screen.is_composited():
            self.set_visual(visual)

    def show_hide(self):
        if self.get_visible():
            self.hide()
        else:
            self.update_ui()
            self.present()

    def quit(self):
        Gtk.main_quit()

class RenameDialog:
    def __init__(self, sender):
        ConfigManager.disable_losefocus_temporary = True
        self.sender = sender

        self.builder = Gtk.Builder()
        self.builder.add_from_file(ConfigManager.data_dir + 'ui/main.ui')
        self.dialog = self.builder.get_object('rename_dialog')

        self.dialog.entry_new_name = self.builder.get_object('entry_new_name')
        self.dialog.entry_new_name.set_text(self.sender.get_label())

        self.dialog.btn_cancel = self.builder.get_object('btn_cancel')
        self.dialog.btn_ok = self.builder.get_object('btn_ok')

        self.dialog.btn_cancel.connect('clicked', lambda w: self.close())
        self.dialog.btn_ok.connect('clicked', lambda w: self.rename())
        self.dialog.entry_new_name.connect('key-press-event', lambda w, x: self.on_keypress(w, x))

        self.dialog.connect('delete-event', lambda w, x: self.close())
        self.dialog.connect('destroy', lambda w: self.close())

        self.dialog.show_all()

    def on_keypress(self, widget, event):
        if Gdk.keyval_name(event.keyval) == 'Return':
            self.rename()

    def close(self):
        ConfigManager.disable_losefocus_temporary = False
        self.dialog.destroy()
        del self

    def rename(self):
        if len(self.dialog.entry_new_name.get_text()) > 0:
            self.sender.set_label(self.dialog.entry_new_name.get_text())

        self.close()

def main():
    GObject.threads_init()
    app = TerminalWin()

    keybinding = GlobalKeyBinding()
    app.keybinding = keybinding
    ConfigManager.ref_keybinding = keybinding
    ConfigManager.ref_show_hide = app.show_hide
    keybinding.connect('activate', lambda w: app.show_hide())
    if not keybinding.grab():
        ConfigManager.set_conf('losefocus-hiding', 'False')
        ConfigManager.set_conf('hide-on-start', 'False')
        app.update_ui()
        msgtext = "Another application using '%s'. Please open preferences and change the shortcut key." % ConfigManager.get_conf('global-key')
        msgbox = Gtk.MessageDialog(app, Gtk.DialogFlags.DESTROY_WITH_PARENT, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, msgtext)
        msgbox.run()
        msgbox.destroy()
    else:
        keybinding.start()
    Gtk.main()

if __name__ == "__main__":
    main()
