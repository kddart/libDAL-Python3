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

__author__ = "alexs"
__copyright__ = "Copyright (C) 2017  Diversity Arrays Technology"
__license__ = "GPL 3.0"
__email__ = ""


class IKddartEntityMeta(object):
    """
    Interface for KDDartEntity meta data, as introspection cannot ascertain data types of class attributes.
    This class also contains the list/get ops for each Entity, and some additional info
    """

    def __init__(self):
        self._tableName = None
        self._attributeDataTypePairs = {}

        # Operation commands for listing/getting/other from DAL
        self._listOps = {}
        self._getOps = {}
        self._otherOps = {}
        self._addOps = {}
        self._delOps = {}
        self._solrOps = {}

    @property
    def attributes(self):
        return self._attributeDataTypePairs

    @property
    def table_name(self):
        return self._tableName

    @property
    def get_ops(self):
        return self._getOps

    @property
    def list_ops(self):
        return self._listOps

    @property
    def other_ops(self):
        return self._getOps

    @property
    def add_ops(self):
        return self._addOps

    @property
    def del_ops(self):
        return self._delOps

    @property
    def solr_ops(self):
        return self._solrOps