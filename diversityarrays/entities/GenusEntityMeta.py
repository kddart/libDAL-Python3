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

from .IKddartEntityMeta import IKddartEntityMeta
from .AttributeDataType import AttributeDataType

__author__ = "alexs"
__copyright__ = "Copyright (C) 2017  Diversity Arrays Technology"
__license__ = "GPL 3.0"
__email__ = ""


class GenusEntityMeta(IKddartEntityMeta):

    def __init__(self):
        super(IKddartEntityMeta, self).__init__()

        self._tableName = "Genus"
        self._attributeDataTypePairs = [
            AttributeDataType("GenotypeName", str, False),
            AttributeDataType("GenusId", int, False),
            AttributeDataType("update", str, False)
        ]

        # Operation commands for listing/getting/other from DAL
        self._listOps = ["/list/genus"]
        self._getOps = ["/get/genus/_id"]
        self._otherOps = ["/update/genus/_id"]
        self._addOps = ["/add/genus"]
        self._delOps = ["/delete/genus/_id"]
        self._solrOps = []
