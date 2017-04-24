#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
"""
 * dalclient library - provides utilities to assist in using KDDart-DAL servers
 * Copyright (C) 2017  Diversity Arrays Technology
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from .GroupControlled import GroupControlled

__author__ = "alexs"
__copyright__ = "Copyright (C) 2017  Diversity Arrays Technology"
__license__ = "GPL 3.0"
__email__ = ""


class AccessControlled(GroupControlled):

    def __init__(self):
        self.super(GroupControlled,).__init__()

        self._accessPerm = None
        self._ownPerm = None
        self._otherPerm = None
        self._ultimatePerm = None

    @property
    def AccessPerm(self):
        return self._accessPerm

    @property
    def OtherPerm(self):
        return self._otherPerm

    @property
    def UltimatePerm(self):
        return self._ultimatePerm

    @property
    def OwnPerm(self):
        return self._ownPerm

    @AccessPerm.setter
    def AccessPerm(self, val):
        self._accessPerm = self.make_numeric(val)

    @OtherPerm.setter
    def OtherPerm(self, val):
        self._otherPerm = self.make_numeric(val)

    @UltimatePerm.setter
    def UltimatePerm(self, val):
        self._ultimatePerm = self.make_numeric(val)

    @OwnPerm.setter
    def OwnPerm(self, val):
        self._ownPerm = self.make_numeric(val)