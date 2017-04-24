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


class DALResponse(object):

    def __init__(self, URL, responseType, rawResponse, recordMeta, statsMeta, translationMap={}):
        self._URL = URL
        self._responseType = responseType
        self._data = []
        self._rawResponse = rawResponse
        self._recordMeta = recordMeta
        self._statsMeta = statsMeta
        self._translationMap = translationMap
        self.output_files = []
        self.returned_ids = []

    def add_response_record(self, responseRecord):
        """
        :param name: Name of key/tag
        :param valuesDict: Dictionary of row data for the ResponseRecord
        :return:
        """
        self._data.append(responseRecord)

    @property
    def response_records(self):
        return self._data

    @property
    def response_type(self):
        return self._responseType

    @property
    def URL(self):
        return self._URL

    @property
    def raw_response(self):
        return self._rawResponse

    @property
    def stats(self):
        return self._statsMeta

    @property
    def meta(self):
        return self._recordMeta

    @property
    def output_files(self):
        return self._outputFiles

    @output_files.setter
    def output_files(self, files):
        self._outputFiles = files

    @property
    def returned_ids(self):
        return self._returnedIds

    @returned_ids.setter
    def returned_ids(self, ids):
        self._returnedIds = ids

    def get_first_record(self):
        if len(self._data) > 0:
            return self._data[0]

        return None

    def visit_response(self, visitor):
        """
        :param visitor: Visitor to visit each response with
        :return:
        """
        for record in self._data:
            if not visitor.visit(record):
                break

    def visit_entities(self, visitor):
        """
        :param visitor: Visitor to visit each response with
        :return:
        """
        for record in self._data:
            if not visitor.visit_with_class(record, self._translationMap):
                break
