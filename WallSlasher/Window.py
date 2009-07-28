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

class MainWin():
    "Main Window"
    session_bus = dbus.SessionBus()

    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file(GLADE_FILE)
        signals_dict = {
            'on_unlock_activate': self.on_unlock_activate,
            'on_backup_activate': self.on_backup_activate,
            'on_restore_activate': self.on_restore_activate,
            'on_apply_activate': self.on_apply_activate,
            'on_quit_activate': self.on_quit_activate,
            'on_about_activate': self.on_about_activate,
        }
        self.builder.connect_signals(signals_dict)
        
        self.main_window = self.builder.get_object('main_window')
        colormap = self.main_window.get_screen().get_rgba_colormap()
        if colormap:
            gtk.widget_set_default_colormap(colormap)
        self.main_window.show_all()

    def on_unlock_activate(self, widget):
        agent = self.session_bus.get_object(
                'org.freedesktop.PolicyKit.AuthenticationAgent', '/')
        xid = self.main_window.window.xid

        try:
            granted = agent.ObtainAuthorization('com.kissuki.wall-slasher',
                    dbus.UInt32(xid), dbus.UInt32(os.getpid()))
        except dbus.exceptions.DBusException:
            return 

        if granted:
            widget.set_sensitive(False)
            self.builder.get_object('backup_action').set_sensitive(True)
            self.builder.get_object('restore_action').set_sensitive(True)
            self.builder.get_object('apply_action').set_sensitive(True)

    def on_backup_activate(self, data):
        print 'backup'

    def on_restore_activate(self, data):
        print 'restore'

    def on_apply_activate(self, data):
        print 'apply'

    def on_quit_activate(self, *args):
        gtk.widget_pop_colormap()
        gtk.main_quit()

    def on_about_activate(self, *args):
        about_dialog = self.builder.get_object('about_dialog')
        about_dialog.run()
        about_dialog.destroy()

    def run(self):
        gtk.main()
