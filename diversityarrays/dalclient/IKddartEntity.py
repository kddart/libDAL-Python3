#!/usr/bin/env/python
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

from diversityarrays.entities.IKddartEntityMeta import IKddartEntityMeta

__author__ = "alexs"
__copyright__ = "Copyright (C) 2017  Diversity Arrays Technology"
__license__ = "GPL 3.0"
__email__ = ""


class IKddartEntity(object):
    """
    Interface for all KddartEntities to implement.
    """

    def __init__(self):

        self._operations = {}
        self._entityId = None
        self._entityIdDownloaded = None
        self._entityMeta = IKddartEntityMeta()

    @property
    def entitiy_id(self):
        return self._entityId

    @property
    def operations(self):
        return self._operations

    @operations.setter
    def operations(self, dict):
        self._operations.update(dict)

    @property
    def attribute_data(self):
        return self._entityMeta.attributes

    @property
    def entity_meta(self):
        return self._entityMeta

    def qualify(self):
        """
        :return: Returns boolean on whether the class attributes matched the entity meta attributes
        """
        for attr in self.entity_meta:
            val = self.__getattribute__(attr.name)

    def contains_attr(self, name):
        """
        :param name: Name of the attribute to check
        :return: Returns the attribute if found
        """
        for attr in self.entity_meta:
            if name is attr.name:
                return attr

            return None