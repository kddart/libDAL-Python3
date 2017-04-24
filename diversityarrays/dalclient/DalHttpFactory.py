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

import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
from .DalRequestImpl import DalRequestImpl

__author__ = "alexs"
__copyright__ = "Copyright (C) 2017  Diversity Arrays Technology"
__license__ = "GPL 3.0"
__email__ = ""


class DalHttpFactory(object):

    def __init__(self):
        print("")

    def create_http_post(self, commandurl, params):
        """
        :param commandurl: url to hit with request
        :param params: POST paramters
        :return: Returns POST DALRequest
        """

        data = urllib.parse.urlencode(params).encode('ascii')
        req = urllib.request.Request(commandurl, data)
        dalreq = DalRequestImpl(req)

        # Switch on for Debuging
        if False:
            for postParam in params.keys():
                print("POST Parameter -> " + str(postParam) + " type: " + str(type(params[postParam])))

        return dalreq

    def create_http_get(self, commandurl):
        """
        :param commandurl: Url to hit with request
        :return: Return GET DALRequest
        """

        req = urllib.request.Request(commandurl)
        req.add_header("Cache-Control", "no-cache")
        dalreq = DalRequestImpl(req)

        return dalreq

    def create_file_upload(self, commandurl, params, random_num, namesinorder, signature, file, encoding='UTF_8'):
        """
        :param commandurl: url to hit with request
        :param params: POST parameters
        :param random_num: random number
        :param namesinorder: names of params in order
        :param signature: hashed signature for upload
        :param file: file for upload
        :param encoding: encoding requires
        :return: returns the DALRequest for the file upload
        """

        data = urllib.parse.urlencode(params).encode("ascii")
        req = urllib.request.Request(commandurl, file, data)
        req.add_header("rand_num", random_num)
        req.add_header("param_order", namesinorder)
        req.add_header("signature", signature)

        dalreq = DalRequestImpl(req)

        return dalreq





