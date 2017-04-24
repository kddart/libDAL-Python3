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

from .IDalRequest import IDalRequest

__author__ = "alexs"
__copyright__ = "Copyright (C) 2017  Diversity Arrays Technology"
__license__ = "GPL 3.0"
__email__ = ""


class DalRequestImpl(IDalRequest):

    def __init__(self, reqIn):
        self._req = reqIn

    @property
    def URI(self):
        """ Returns the URI for the Dal HttpRequest """
        return self._req.get_full_url()

    @property
    def all_headers(self):
        """ Returns the URI for the Dal HttpRequest """
        return self._req.get_data()

    @property
    def request(self):
        """ Returns the HttpRequest itself """
        return self._req
