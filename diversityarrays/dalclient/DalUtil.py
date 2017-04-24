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

import uuid
import hashlib
import hmac
import json
from .DALResponseFormatException import DALResponseFormatException
import _elementtree as cElementTree
from .DALXmlConfig import DALXmlConfig
from .DALResponse import DALResponse
from .DALResponseRecord import DALResponseRecord
from .IDALClient import IDALClient
from .DALResponseException import DALResponseException

__author__ = "alexs"
__copyright__ = "Copyright (C) 2017  Diversity Arrays Technology"
__license__ = "GPL 3.0"
__email__ = ""


class DalUtil:

    def create_random_number(self):
        """
        :return: 64 bit random number for signature
        """
        return uuid.uuid4().int & (1 << 64) - 1

    def create_sha1_hash(self, hashkey, hashable):
        """
           :param writekey: Write token from DAL
           :param dataforsig: Data to be hashed
           :return: hashed signature
        """

        sha_1 = hashlib.sha1
        hashkey = bytes(hashkey.encode('ascii'))
        hashable = bytes(hashable.encode('ascii'))

        hashed = hmac.new(hashkey, hashable, digestmod=sha_1)
        signature = hashed.hexdigest()

        return signature

    def compute_MD5_checksum(self, writeKey, file):
        """
        :param writeKey: Write token from DAL
        :param file: File to be hashed using MD5
        :return: hashed MD5 signature
        """

        md5 = hashlib.md5()
        hashed = hmac.new(writeKey, file, digestmod=md5)
        signature = hashed.hexdigest()

        return signature

    def parse_response(self, url, responseType, response, translationMap={}, errorCode=None):
        """
        :param responseType: Json or XML response content format
        :param response: Actual response content
        :return: Dict of values seen in response content
        """
        recordInfo = {}
        recordMeta = {}
        recordData = {}
        recordFiles = []
        returnedIds = []

        if type(response) == type([]):
            response = "".join(map(str, response))

        if responseType.isXML():
            data = self.handle_xml(response)
        else:
            data = self.handle_json(response)

        if IDALClient.TAG_RECORD_ERROR in list(data.keys()):
            message = "DAL Returned : " + str(errorCode) + ": "
            for error in data[IDALClient.TAG_RECORD_ERROR]:
                for key in list(error.keys()):
                    message += key + " - " + error[key] + " "
            raise DALResponseException(message)

        if IDALClient.TAG_OUTPUT_FILE in list(data.keys()):
            recordFiles = data[IDALClient.TAG_OUTPUT_FILE]

        if IDALClient.TAG_STAT_INFO in list(data.keys()):
            recordInfo = data[IDALClient.TAG_STAT_INFO][0]

        if IDALClient.TAG_INFO in list(data.keys()):
            for tag in data[IDALClient.TAG_INFO]:
                recordInfo.update(tag)

        if IDALClient.TAG_RETURN_ID in list(data.keys()):
            returnedIds = returnedIds + data[IDALClient.TAG_RETURN_ID]

        if IDALClient.TAG_RECORD_META in list(data.keys()):
            recordMeta = data[IDALClient.TAG_RECORD_META][0]
            recordData = data[recordMeta[IDALClient.TAG_NAME]]

            #Adds in virtual column data
            if IDALClient.TAG_VCOL in list(data.keys()):
                if len(data[IDALClient.TAG_VCOL]) >= 1:
                    vcols = data[IDALClient.TAG_VCOL][0]
                    recordData.updat(vcols)

        response = DALResponse(url, responseType, response, recordMeta, recordInfo, translationMap)
        if not recordFiles is None:
            response.output_files = recordFiles

        if not returnedIds is None:
            response.returned_ids = returnedIds

        if not recordData is None:
            for el in recordData:
                response.add_response_record(DALResponseRecord(recordMeta[IDALClient.TAG_NAME], el))

        return response

    def handle_xml(self, response, debug=0):
        """
        :param response: Response content
        :return: Dict of response content
        """
        if not type(response) is type(""):
            response = str(response.decode("utf-8"))

        root = cElementTree.XML(response)
        data = DALXmlConfig().parse(root)

        if data is None:
            raise DALResponseFormatException("Input content for parsing from xml was None")

        return data

    def handle_json(self, response, debug=0):
        """
        :param response: Response content
        :return: Dict of response content
        """
        if not type(response) is type(""):
            response = str(response.decode("utf-8"))

        data = json.loads(response)

        if data is None:
            raise DALResponseFormatException("Input content for parsing from json was None")

        return data

