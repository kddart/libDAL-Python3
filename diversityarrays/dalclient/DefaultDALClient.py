#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
"""
 * dalclient library - provides utilities to assist in using KDDart-DAL servers
 * Copyright (C) 2015,2016,2017  Diversity Arrays Technology
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

from .IDALClient import IDALClient
from .ResponseType import ResponseType
from .DALResponseException import DALResponseException
from .SessionExpire import SessionExpire
from .HttpPostBuilder import HttpPostBuilder
from .DalHttpFactory import DalHttpFactory
import os
import sys
import urllib.request, urllib.error, urllib.parse
from .DalUtil import DalUtil
import http.cookiejar
import logging
logger = logging.getLogger(__name__)

__author__ = "alexs"
__copyright__ = "Copyright (C) 2015,2016,2017  Diversity Arrays Technology"
__license__ = "GPL 3.0"


class DefaultDALClient(IDALClient):

    def __init__(self, debug=0):
        super().__init__()

        # For backwards compatibility: if debug > 0, print any debug log
        # messages emitted by diversityarrays.dalclient loggers to stdout
        if debug > 0:
            parent_package_name = __name__.rsplit(".", maxsplit=1)[0]
            parent_logger = logging.getLogger(parent_package_name)
            # Avoid doubling up handlers if multiple instances are constructed:
            if not parent_logger.handlers:
                parent_logger.addHandler(logging.StreamHandler(sys.stdout))
                parent_logger.setLevel(logging.DEBUG)

        self._dalUtil = DalUtil()

        # For cookie management between commands
        self._cookiejar = http.cookiejar.CookieJar()
        self._opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self._cookiejar))

        self._loginURL = None
        self._loggedIn = False

        self._LIST_GROUP_CMD = "list/group"
        self._SWITCH_GROUP_CMD = "switch/group/"

        # Content Type
        self._responseType = ResponseType(False)

        self._switchGroup = True

        # Default will sign you out eventually
        self._expire = SessionExpire().timeout()

        # Post Builder and post Factory
        self._dalHttpFactory = DalHttpFactory()

        # Info from login response
        self._writeToken = None
        self._cookie = None
        self._userName = None
        self._userId = None
        self._groupId = None
        self._groupName = None
        self._isAdmin = None

    @property
    def reponse_type(self):
        """
        :return: json or XML response type return
        """
        return self._responseType

    @reponse_type.setter
    def reponse_type(self, reponseType):
        """
        :param reponseType: Set response type to Json or XML
        :return: this DalClient
        """
        self._responseType = reponseType

    @property
    def auto_switch_group(self):
        """
        :return: If the group is automatically switched on login to first in list
        """
        return self._switchGroup

    @auto_switch_group.setter
    def auto_switch_group(self, switchGroupYes):
        """
        :param switchGroupYes: true/false for whether the first listed group is selected
        :return: returns this DALclient
        """
        self._switchGroup = switchGroupYes

    @property
    def session_expiry_option(self):
        """
        :return: Returs if an excplicit logout is required or not
        """
        return self._expire

    @session_expiry_option.setter
    def session_expiry_option(self, option):
        """
        :param option: Whether the session needs to be excplicitly logged out of or if there is an expiry
        :return:
        """
        self._expire = option

    def is_logged_in(self):
        """
        :return: Returns true/false for whether the client is current logged in
        """
        return self._loggedIn

    @property
    def URL(self):
        """
        :param URL: URL to try for login
        :return:
        """
        return self._loginURL

    @URL.setter
    def URL(self, URL):
        """
        :param URL: URL to try for login
        :return:
        """
        self._loginURL = URL

    def login(self, username, password):
        """
        :param username: System username
        :param password: System password
        :return:
        """
        self.login_internal(username, password, False)

    def login_using_oAuth2(self, oAuth2Token, redirectUrl):
        """
        :param oAuth2Token: Google oAuth2Token for login
        :param redirectUrl: Valid redirect url for token
        :return:
        """
        self.login_internal(None, None, True, oAuth2Token, redirectUrl)

    def login_internal(self, username, password, usingOAuth2, oAuth2Token=None, redirectUrl=None):
        """
        :param username: System username
        :param password: System password
        :param usingOAuth2: Boolean as to whether to use google oAuth2 instead of system login
        :param oAuth2Token: Tokean for oAuth2 login, is selected
        :return:
        """
        # If there no URL we can conitnue?
        if self._loginURL is None:
            raise DALResponseException("Login URL is None")

        # Can ignore the hashing if using oAuth2 to login
        cmd = None;
        url = None;
        if not usingOAuth2:
            cmd = "login/" + username + "/" + self._expire
            url = self._loginURL + "/" + cmd

            # Perform hashing!
            rand = str(self._dalUtil.create_random_number())
            signature = self._dalUtil.create_sha1_hash(hashkey=password, hashable=username)
            signature = self._dalUtil.create_sha1_hash(hashkey=signature, hashable=rand)
            signature = self._dalUtil.create_sha1_hash(hashkey=signature, hashable=url)
        else:
            signature = None
            cmd = "oauth2google"
            url = self._loginURL + "/" + cmd

        httpPostBuilder = HttpPostBuilder(self._dalHttpFactory, url)

        logger.debug("Attempting login to %s", self._loginURL)
        logger.debug("Using cmd: %s", url)
        if signature is not None:
            logger.debug("Hash: %s\n", signature)

        request = httpPostBuilder.set_respone_type(self._responseType)
        request = request.add_parameter("rand_num", rand) \
            .add_parameter("url", url) \
            .add_parameter("ctype", self._responseType.value)
        if not usingOAuth2:
            request.add_parameter("signature", signature)
        else:
            request.add_parameter("access_token", oAuth2Token) \
            .add_parameter("redirect_url", redirectUrl)

        request = request.build()

        # Actually performing the Http command
        rsp = None
        content = None
        try:
            rsp = self._opener.open(request.request)
            content = rsp.read()
        except urllib.error.HTTPError as e:
            self.build_DALResponse(e.read(), e.getcode())
        finally:
            if not rsp is None:
                rsp.close()

        if content is None:
            raise DALResponseException("No Meta seen in response")

        content = str(content.decode("utf-8"))

        # Populated global attributes
        if not self._responseType.isXML():
            response = self._dalUtil.handle_json(content)
        else:
            response = self._dalUtil.handle_xml(content)

        self._userName = response["User"][0][self.ATTR_USER_NAME]
        self._userId = response["User"][0][self.ATTR_USER_ID]
        self._writeToken = response[self.TAG_WRITE_TOKEN][0]["Value"]

        if self._switchGroup:
            self.switch_to_first_group()

    def switch_to_first_group(self):
        """
        :return:
        """
        dalResponse = self.perform_query(self._LIST_GROUP_CMD)
        dalElement = dalResponse.get_first_record()

        if dalElement is None:
            raise DALResponseException("No Group-Meta seen in response for switching groups")

        groupName = dalElement.rowdata["SystemGroupName"]
        groupId = dalElement.rowdata["SystemGroupId"]
        result = self.switch_group(groupId)

        self._groupName = groupName
        self._groupId = int(groupId)

        logger.debug("Switched to group: %s successfully", groupName)

    def logout(self):
        """
        :return:
        """
        response = self.perform_query("/logout")

        logger.debug("Logged out")

        self._loggedIn = False
        self._userId = None
        self._userName = None
        self._groupName = None
        self._groupId = None

    def switch_group(self, groupId):
        """
        :param grouId: Id of group to switch into from current group
        :return:
        """
        cmd = self._SWITCH_GROUP_CMD + groupId
        self.perform_query(cmd)

    @property
    def user_id(self):
        """
        :return: User of Id for the current logon
        """
        return self._userId

    @property
    def user_name(self):
        """
        :return: Returns the name of the currently logged in user
        """
        return self._userName

    @property
    def write_token(self):
        """
        :return: Gets the write token for the current login
        """
        return self._writeToken

    def is_an_admin(self):
        """
        :return: Returns true/false for whether the currently logged in user is an admin
        """
        raise NotImplementedError

    @property
    def group_name(self):
        """
        :return: Returns the name of currently logged in user group
        """
        return self._groupName

    @property
    def group_id(self):
        """
        :return: Returns the id of the current logged in user group
        """
        return self._groupId

    def perform_query(self, command):
        """
        :param command: Command for DAL
        :return: Returns DALResponse for the command
        """
        return self.perform_query_internal(command, False)

    def perform_query_internal(self, command, postTrue, postParams=None, fileContentTypeTuple=None, dont_include=None):
        """
        :param command: Command for DAL
        :return: Returns DALResponse for the command
        """
        cmd = self._loginURL + "/" + command

        if not self._responseType.isXML() and not dont_include:
            cmd += "?ctype=" + self._responseType.value

        prep = HttpPostBuilder(self._dalHttpFactory, cmd) \
        .set_respone_type(self._responseType) \

        data = None
        if not fileContentTypeTuple is None and not postParams is None:
            data = fileContentTypeTuple[1]

            postParams['Content-type'] = fileContentTypeTuple[0]
            postParams['Content-length'] = len(data)

        if not postParams is None and len(postParams) > 0:
            for key in postParams.keys():
                val = postParams[key]
                prep = prep.add_parameter(key, val)

        if postTrue and not fileContentTypeTuple is None:
            # Building for a POST with an upload file
            req = prep.build_for_upload(self._writeToken, data)

        elif postTrue:
            # Building for a POST
            req = prep.build_for_update(self._writeToken)
        else:
            # Building for a GET
            req = prep.build()

        logger.debug("Performing Query: %s", cmd)

        # Actually performing the Http command
        content = ""
        rsp = None
        try:
            rsp = self._opener.open(req.request)
            content = rsp.read()
        except urllib.error.HTTPError as e:
            content = e.read()
            return self.build_DALResponse(content, e.getcode())

        finally:
            if not rsp is None:
                rsp.close()

        if content is None:
            raise DALResponseException("No Meta seen in response")

        content = str(content.decode("utf-8"))

        return self.build_DALResponse(content)

    def perpare_GET_query(self, command):
        """
        :param command: GET command for DAL
        :return:
        """
        builder = HttpPostBuilder(command, self._dalHttpFactory)
        builder.build()

    def prepare_POST_query(self, command):
        """
        :param command: POST command for DAL
        :return:
        """
        builder = HttpPostBuilder(command, self._dalHttpFactory)
        builder.build_for_update(self._writeToken)

    def perform_update(self, command, postParams):
        """
        :param command: POST command for the DAL
        :param postParams: Post parameters containing the update info
        :return: Returns DALReponse for the command
        """
        return self.perform_query_internal(command, True, postParams)

    def prepare_update(self, command):
        """
        :param command: POST command for the DAL
        :return:
        """
        builder = HttpPostBuilder(command, self._dalHttpFactory)
        builder.build_for_update(self._writeToken)

    def perform_upload(self, command, postParams, uploadable):
        """
        :param command: POST command for the DAL
        :param postParams: Post parameters to accompany the upload file
        :param uploadable: File/stream to be uploaded
        :return: Returns the DALResponse for the command
        """
        return self.perform_query_internal(command, True, postParams, uploadable)

    def prepare_upload(self, command, uploadable):
        """
        :param command: POST command for the DAL
        :return:
        """
        builder = HttpPostBuilder(command, self._dalHttpFactory)
        builder.build_for_upload(self._writeToken, uploadable)

    def prepare_export(self, command):
        """
        :param command: DAL command for export
        :return:
        """
        builder = HttpPostBuilder(command, self._dalHttpFactory)
        builder.build()

    def perform_export(self, command, postParams):
        """
        :param command: DAL command for export
        :param postParams: Post parameters for the query
        :return: Returns the DALResponse for the query
        """
        return self.perform_query_internal(command, True, postParams)

    @property
    def cookie(self):
        """
        :return: Returns the cookie for the session with DAL
        """
        return self._cookiejar

    def download_file(self, fileUrl, localFile=None):
        """
        :param fileURL: DAL file url
        :param localFile: File to dump download contents into
        :return: Returns the file content
        """
        content = "No Content Found."

        # Actually performing the Http command
        rsp = None
        try:
            rsp = self._opener.open(fileUrl)
            content = rsp.read()

            if not localFile is None:
                # Open our local file for writing
                with open(os.path.basename(localFile), "wb") as local_file:
                    local_file.write(content)

        except urllib.error.HTTPError as e:
            content = self.build_DALResponse(e.read(), e.getcode())

        finally:
            if not rsp is None:
                rsp.close()

        if content is None:
            raise DALResponseException("No Meta seen in response")

        return content

    def build_DALResponse(self, httpResponse, errorCode=200):
        """
        :param httpResponse: Result from DAL yet to be translated into a DALResponse Object
        :return: Returns the constructed DALResponse
        """
        response = self._dalUtil.parse_response(self._loginURL, self._responseType, httpResponse, self.TAG_NAME_TO_CLASS_NAME, errorCode)

        if errorCode is None:
            response.set_error_code(errorCode)

        return response
