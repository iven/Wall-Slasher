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

from WallSlasher.Constants import *
from WallSlasher.PolkitAction import PolkitAction

class MainWin():
    "Main Window"

    def __init__(self):
        builder = gtk.Builder()
        builder.add_from_file(GLADE_FILE)
        signals_dict = {
            'on_unlock_activate': self.on_unlock_activate,
            'on_backup_activate': self.on_backup_activate,
            'on_restore_activate': self.on_restore_activate,
            'on_apply_activate': self.on_apply_activate,
            'on_quit_activate': self.on_quit_activate,
        }
        builder.connect_signals(signals_dict)
        
        main_window = builder.get_object('main_window')
        colormap = main_window.get_screen().get_rgba_colormap()
        if colormap:
            gtk.widget_set_default_colormap(colormap)
        main_window.show_all()

        self.unlock_action = PolkitAction(main_window)

    def on_unlock_activate(self, widget):
        if self.unlock_action.authenticate():
            widget.set_sensitive(False)

    def on_backup_activate(self, data):
        print 'backup'

    def on_restore_activate(self, data):
        print 'restore'

    def on_apply_activate(self, data):
        print 'apply'

    def on_quit_activate(self, *args):
        gtk.widget_pop_colormap()
        gtk.main_quit()

    def run(self):
        gtk.main()
