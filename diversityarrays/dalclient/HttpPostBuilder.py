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

from .DalUtil import  DalUtil

__author__ = "alexs"
__copyright__ = "Copyright (C) 2017  Diversity Arrays Technology"
__license__ = "GPL 3.0"
__email__ = ""


class HttpPostBuilder:


    def __init__(self, dalhttpfactory, dalCommandUrl, logger=None):

        self._chartset = None
        self._dalUtil = DalUtil()

        # Response type (.json or .xml)
        self._responsetype = None

        # Post params are to be kept in order
        self._collectedPairs = dict()

        self._factory = dalhttpfactory
        self._commandUrl = dalCommandUrl
        self._log = logger

    def set_respone_type(self, type):
        """
        :param type: Type is either Json or XML
        :return:
        """
        self._responsetype = type

        return self

    def add_parameter(self, name, value):
        self._collectedPairs[name] = value

        return self

    def add_parameters(self, dict):
        for name in list(dict.keys()):
            self._collectedPairs[name] = dict[name]

        return self

    def build(self):
        """
        :return: Returns HttpPost request for collected pairs (not update)
        """
        if not self._responsetype.isXML():
            self._collectedPairs["ctype"] = self._responsetype.value

        return self._factory.create_http_post(self._commandUrl, self._collectedPairs)

    def build_for_update(self, writetoken):
        """
        :param writetoken: Write taken for hash taken from DAL
        :return: Post request is returned (for update)
        """
        return self._factory.create_http_post(self._commandUrl, self.collect_pairs_for_update(writetoken))

    def collect_pairs_for_update(self, writekey, returnedSig=None):
        """ Collecting the pairs in a format that works with DAL (no None's)
        :param writekey: Write token taken from dal
        :param returnedsig: returned signature if wanted
        :return: new post parameter pairs
        """
        rand = self._dalUtil.create_random_number()

        dataForSig = self._commandUrl + str(rand)
        namesInOrder = ""

        for name in list(self._collectedPairs.keys()):
            val = self._collectedPairs[name]
            if val is None:
                val = ""

            namesInOrder += name + ","
            dataForSig += val

        if not returnedSig is None:
            returnedSig += dataForSig

        signature = self._dalUtil.create_sha1_hash(str(writekey), str(dataForSig))

        # Preparing post params
        forPost = dict()
        forPost["rand_num"] = str(rand)
        forPost["url"] = self._commandUrl
        forPost["param_order"] = namesInOrder
        forPost["signature"] = signature

        forPost.update(self._collectedPairs)

        if not self._responsetype.isXML():
            forPost["ctype"] = self._responsetype.value

        return forPost

    def build_for_upload(self, writekey, fileForUpload):
        """
        :param writekey: Write token from DAL
        :param fileForUpload: File to be uploaded
        :return: returns the POST DALRequest for file upload
        """
        rand = self._dalUtil.create_random_number()
        md5CheckSum = self._dalUtil.compute_MD5_checksum(fileForUpload)

        dataForSig = self._commandUrl + str(rand)
        namesInOrder = ""

        for name in list(self._collectedPairs.keys()):
            val = self._collectedPairs[name]
            if val is None:
                val = ""

            namesInOrder += name + ","
            dataForSig += val

        dataForSig += md5CheckSum
        signature = self._dalUtil.create_sha1_hash(writekey, dataForSig)

        return self._factory.create_file_upload(self._commandUrl, self._collectedPairs, rand, namesInOrder, signature, fileForUpload)



