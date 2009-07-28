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

import os
import dbus

class PolkitAction:
    session_bus = dbus.SessionBus()

    def __init__(self, widget):
        self.widget = widget

    def authenticate(self):
        agent = self.session_bus.get_object('org.freedesktop.PolicyKit.AuthenticationAgent', '/')
        xid = self.widget.get_toplevel().window.xid

        try:
            granted = agent.ObtainAuthorization('com.kissuki.wall-slasher', dbus.UInt32(xid), dbus.UInt32(os.getpid()))
        except dbus.exceptions.DBusException:
            return False
        else:
            return granted
