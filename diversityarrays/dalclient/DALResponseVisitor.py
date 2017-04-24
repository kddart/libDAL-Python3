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
from .DALEntityBuilder import DALEntityBuilder

__author__ = "alexs"
__copyright__ = "Copyright (C) 2017  Diversity Arrays Technology"
__license__ = "GPL 3.0"
__email__ = ""


class DALResponseVisitor(object):

    def __init__(self, visitorFunction):

        self._builder = DALEntityBuilder()
        self._visitorFunction = visitorFunction

    def visit(self, responseRecord):
        """
        :param responseRecord: Response record function passed in with which the visitor function visits
        :return:
        """
        return self._visitorFunction(responseRecord)

    def visit_with_class(self, responseRecord, translationMap):
        """
        :param responseRecord: Response record function passed in with which the visitor function visits
        :return:
        """
        rowdata = responseRecord.rowdata
        dynamicClass = self._builder.build_entity(responseRecord.key_name, rowdata)

        return self._visitorFunction(dynamicClass)
