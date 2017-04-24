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

from .IKddartEntity import IKddartEntity
from .AccessControlled import AccessControlled

__author__ = "alexs"
__copyright__ = "Copyright (C) 2017  Diversity Arrays Technology"
__license__ = "GPL 3.0"
__email__ = ""


class DALEntityBuilder(object):

    def __init__(self):
        """
        The following are special exceptions for specific field names
        """

        # Params to be ignored
        self._toIgnore = [
        ]

        # Params the are actually permissions
        self._permissions = [
            "UltimatePerm",
            "AccessPerm",
            "OwnPerm",
            "OtherPerm",
            "GroupId"
        ]

    def build_entity(self, keyname, rowdata, translationMap={}):
        """
        :param keyname: Name of the dynamically generated class
        :param rowdata: Row data (attributes) for the generated class
        :return: Returns the created entity, which implements both IKDDartEntity and AccessControlled
        """
        postParseAttrs = {}
        commands = {}
        rowdataFinal = {}

        unusedData = []

        # Processing entities row data for nested dat and exceptions
        for key in rowdata.keys():
            value = rowdata[key]

            # Is dictionary therefore its a nested entity! Create new Entity!
            if type(value) == type([]):
                if len(value) > 0:
                    list = []
                    for val in value:
                        if type(val) == type(dict()):
                            nestedent = self.build_entity(key, val)
                            list.append(nestedent)
                        else:
                            unusedData.append(val)
                    rowdataFinal[key] = list

                continue

            # Is a permission! handle differently
            if key in self._permissions:
                postParseAttrs[key] = rowdata[key]
                continue

            # Is an Ignore! Do nothing
            if key in self._toIgnore:
                continue

            # This is a command for the entity!
            if not key[0].isupper():
                commands[key] = rowdata[key]
                continue

            # Finally if normal attr, then add to final dict
            rowdataFinal[key] = value
        rowdataFinal["UnusedData"] = unusedData

        # Building class and setting attributes gathered for special entry (Integers)
        if not translationMap is None and len(translationMap) > 0 and keyname in translationMap.keys() :
            keyname = translationMap[keyname]

        dynamicClass = type(str(keyname), (IKddartEntity, AccessControlled), rowdataFinal)

        for name in postParseAttrs.keys():
            value = postParseAttrs[name]
            setattr(dynamicClass, name, value)

        dynamicClass.operations = commands

        return dynamicClass

    def removekey(self, dict, key):
        r = dict(dict)
        del r[key]
        return r
