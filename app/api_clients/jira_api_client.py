# -*- coding: utf-8 -*-

#
# Unless explicitly stated otherwise all files in this repository are licensed
# under the Apache 2 License.
#
# This product includes software developed at Datadog
# (https://www.datadoghq.com/).
#
# Copyright 2018 Datadog, Inc.
#

"""jira_api_client.py

Concrete class representing Jira API Client.
"""

from os import environ

from jira import JIRA, JIRAError
from func_timeout import func_set_timeout, FunctionTimedOut
from . import APIClient


class JIRAAPIClient(APIClient):
    """
    This class provides an API client to interact with the JIRA API
    """

    def __init__(self):
        self.err = self.initialize()

    @func_set_timeout(4)
    def _return_client(self, server, username, key):
        return JIRA(
            server=server,
            basic_auth=(username, key),
            max_retries=2,
        )

    def initialize(self):
        server = environ.get('JIRA_SERVER_ADDRESS')
        username = environ.get('JIRA_USERNAME')
        key = environ.get('JIRA_API_KEY')

        self._client = None

        if bool(server) and bool(username) and bool(key):
            try:
                self._client = self._return_client(server, username, key)
                return None
            except FunctionTimedOut:
                return "Could not connect to JIRA server"
            except JIRAError as err:
                to_return = "Error occurred when connecting to JIRA server: " + err.text
                if err.text == "Basic auth with password is not allowed on this instance\n":
                    to_return += "\nPerhaps the provided authentication is invalid?"
                return to_return

    def client(self):
        return self._client
