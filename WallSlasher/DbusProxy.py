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

import dbus
from WallSlasher.Constants import INTERFACE, PATH

class DbusProxy:
    try:
        __system_bus = dbus.SystemBus()
        __proxy = __system_bus.get_object(INTERFACE, PATH)
    except dbus.exceptions.DBusException:
        __proxy = None

    def __getattr__(self, name):
        return self.__proxy.get_dbus_method(name, INTERFACE)

proxy = DbusProxy()
