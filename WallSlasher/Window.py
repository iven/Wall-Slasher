#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# This file is part of Wall Slasher.

# Wall Slasher is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Wall Slasher is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author(s): Iven Day (Xu Lijian) <ivenvd@gmail.com>
# Copyright (C) 2009 Iven Day

import pygtk
pygtk.require('2.0')
import gtk
import dbus
import os

from WallSlasher.Constants import *
from WallSlasher.PolkitAction import PolkitAction
from WallSlasher.DbusProxy import proxy

class MainWin():
    "Main Window"
    session_bus = dbus.SessionBus()

    def __init__(self):
        builder = gtk.Builder()
        builder.add_from_file(GLADE_FILE)
        signals_dict = {
            'on_unlock_activate': self.on_unlock_activate,
            'on_backup_activate': self.on_backup_activate,
            'on_restore_activate': self.on_restore_activate,
            'on_apply_activate': self.on_apply_activate,
            'on_quit_activate': self.on_quit_activate,
            'on_about_activate': self.on_about_activate,
        }
        builder.connect_signals(signals_dict)
        
        self.main_window = builder.get_object('main_window')
        colormap = self.main_window.get_screen().get_rgba_colormap()
        if colormap:
            gtk.widget_set_default_colormap(colormap)
        self.main_window.show_all()
        
        self.xid = self.main_window.window.xid
        self.backup_action = builder.get_object('backup_action')
        self.restore_action = builder.get_object('restore_action')
        self.apply_action = builder.get_object('apply_action')

    def backup_file_exists(self):
        return os.path.exists(BACKUP_FILE)

    def on_unlock_activate(self, widget):
        agent = self.session_bus.get_object(
                'org.freedesktop.PolicyKit.AuthenticationAgent', '/')
        try:
            granted = agent.ObtainAuthorization(POLICYKIT_INTERFACE,
                    dbus.UInt32(self.xid), dbus.UInt32(os.getpid()))
        except dbus.exceptions.DBusException:
            granted = False
        if granted:
            widget.set_sensitive(False)
            self.backup_action.set_sensitive(True)
            self.apply_action.set_sensitive(True)
            if self.backup_file_exists():
                self.restore_action.set_sensitive(True)

    def on_backup_activate(self, data):
        if self.backup_file_exists():
            dialog = gtk.MessageDialog(self.main_window, gtk.DIALOG_MODAL,
                    gtk.MESSAGE_WARNING, gtk.BUTTONS_YES_NO,
                    "文件已存在，是否覆盖？")
            result = dialog.run()
            dialog.destroy()
            if result != gtk.RESPONSE_YES:
                return
        proxy.backup()
        self.restore_action.set_sensitive(True)

    def on_restore_activate(self, data):
        dialog = gtk.MessageDialog(self.main_window, gtk.DIALOG_MODAL,
                gtk.MESSAGE_WARNING, gtk.BUTTONS_OK_CANCEL,
                "操作不可恢复，确定继续？")
        result = dialog.run()
        dialog.destroy()
        if result == gtk.RESPONSE_OK:
            proxy.restore()

    def on_apply_activate(self, data):
        print 'apply'

    def on_quit_activate(self, *args):
        proxy.exit()
        gtk.widget_pop_colormap()
        gtk.main_quit()

    def on_about_activate(self, *args):
        about_dialog = self.builder.get_object('about_dialog')
        about_dialog.run()
        about_dialog.destroy()

    def run(self):
        gtk.main()
