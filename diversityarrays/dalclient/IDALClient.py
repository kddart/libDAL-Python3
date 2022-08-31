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

import os

__author__ = "alexs"
__copyright__ = "Copyright (C) 2017  Diversity Arrays Technology"
__license__ = "GPL 3.0"
__email__ = ""


class IDALClient:

    # Instance Tag fields
    TAG_USER = "User"
    TAG_WRITE_TOKEN = "WriteToken"
    TAG_INFO = "Info"
    TAG_STAT_INFO = "StatInfo"
    TAG_ERROR = "Error"
    TAG_RECORD_META = "RecordMeta"
    TAG_RECORD_ERROR = "Error"
    TAG_NAME = "TagName"
    TAG_VCOL = "VCol"
    TAG_OPERATION = "TagOperation"
    TAG_PAGINATION = "Pagination"
    TAG_RETURN_ID = "ReturnId"
    TAG_RETURN_ID_FILE = "ReturnIdFile"
    TAG_OUTPUT_FILE = "OutputFile"

    # Instance Attributes
    ATTR_VALUE = "Value"
    ATTR_USER_ID = "UserId"
    ATTR_USER_NAME = "UserName"
    ATTR_VERSION = "Version"
    ATTR_GROUP_NAME = "GroupName"
    ATTR_GROUP_ID = "GroupId"
    ATTR_GADMIN = "GAdmin"
    ATTR_GROUP_SELECTION_STATUS = "GroupSelectionStatus"
    ATTR_LOGIN_STATUS = "LoginStatus"
    ATTR_MESSAGE = "Message"
    ATTR_REST = "REST"
    ATTR_NUM_OF_RECORDS = "NumOfRecords"
    ATTR_NUM_OF_PAGES = "NumOfPages"
    ATTR_NUM_PER_PAGE = "NumPerPages"
    ATTR_PAGE = "Page"
    ATTR_PARA_NAME = "ParaName"
    ATTR_XML = "xml"

    # Naming exception mapping for entity creation
    TAG_NAME_TO_CLASS_NAME = {
        "TrialTrait":"Trait",
        "User":"SystemUser"}

    # Exception file where naming exceptions are kept
    TAG_EXCEPTION_FILE = "TagToClassName.properties"

    @property
    def reponse_type(self):
        """
        :return: json or XML response type return
        """
        raise NotImplementedError

    @reponse_type.setter
    def reponse_type(self, reponseType):
        """
        :param reponseType: Set response type to Json or XML
        :return: this DalClient
        """
        raise NotImplementedError

    @property
    def auto_switch_group(self):
        """
        :return: If the group is automatically switched on login to first in list
        """
        raise NotImplementedError

    @auto_switch_group.setter
    def auto_switch_group(self, switchGroupYes):
        """
        :param switchGroupYes: true/false for whether the first listed group is selected
        :return: returns this DALclient
        """
        raise NotImplementedError

    @property
    def session_expiry_option(self):
        """
        :return: Returs if an excplicit logout is required or not
        """
        raise NotImplementedError

    @session_expiry_option.setter
    def session_expiry_option(self, option):
        """
        :param option: Whether the session needs to be excplicitly logged out of or if there is an expiry
        :return:
        """
        raise NotImplementedError

    def is_logged_in(self):
        """
        :return: Returns true/false for whether the client is current logged in
        """
        raise NotImplementedError

    @property
    def URL(self):
        """
        :param URL: URL to try for login
        :return:
        """
        raise NotImplementedError


    @URL.setter
    def URL(self, URL):
        """
        :param URL: URL to try for login
        :return:
        """
        raise NotImplementedError

    def login(self, username, password):
        """
        :param username: The user name for login
        :param password: The password for login
        :return:
        """
        raise NotImplementedError

    def login_using_oAuth2(self, token, redirectUrl):
        """
        :param oAuth2Token: Google oAuth2Token for login
        :param redirectUrl: Valid redirect url for token
        :return:
        """
        raise NotImplementedError

    def logout(self):
        """
        :return:
        """
        raise NotImplementedError

    def switch_group(self, grouId):
        """
        :param grouId: Id of group to switch into from current group
        :return:
        """
        raise NotImplementedError

    @property
    def user_id(self):
        """
        :return: User of Id for the current logon
        """
        raise NotImplementedError

    @property
    def user_name(self):
        """
        :return: Returns the name of the currently logged in user
        """
        raise NotImplementedError

    @property
    def write_token(self):
        """
        :return: Gets the write token for the current login
        """
        raise NotImplementedError

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
        raise NotImplementedError

    @property
    def group_id(self):
        """
        :return: Returns the id of the current logged in user group
        """
        raise NotImplementedError

    def perform_query(self, command):
        """
        :param command: Command for DAL
        :return: Returns DALResponse for the command
        """
        raise NotImplementedError

    def perpare_GET_query(self, command):
        """
        :param command: GET command for DAL
        :return:
        """
        raise NotImplementedError

    def prepare_POST_query(self, command):
        """
        :param command: POST command for DAL
        :return:
        """
        raise NotImplementedError

    def perform_update(self, command, postParams):
        """
        :param command: POST command for the DAL
        :param postParams: Post parameters containing the update info
        :return: Returns DALReponse for the command
        """
        raise NotImplementedError

    def prepare_update(self, command):
        """
        :param command: POST command for the DAL
        :return:
        """
        raise NotImplementedError

    def perform_upload(self, command, postParams, uploadable):
        """
        :param command: POST command for the DAL
        :param postParams: Post parameters to accompany the upload file
        :param uploadable: File/stream to be uploaded
        :return: Returns the DALResponse for the command
        """
        raise NotImplementedError

    def prepare_upload(self, command, uploadable):
        """
        :param command: POST command for the DAL
        :param uploadable: File/stream to be uploaded
        :return:
        """
        raise NotImplementedError

    def prepare_export(self, command):
        """
        :param command: DAL command for export
        :return:
        """
        raise NotImplementedError

    def perform_export(self, command, postParams):
        """
        :param command: DAL command for export
        :param postParams: Post parameters for the query
        :return: Returns the DALResponse for the query
        """
        raise NotImplementedError

    def download_file(self, fileUrl):
        """
        :param fileURL: DAL file url
        :return: Returns the file content
        """
        raise NotImplementedError

    @property
    def cookie(self):
        """
        :return: Returns the cookie for the session with DAL
        """
        raise NotImplementedError











