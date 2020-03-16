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

"""trello_api_client.py

Concrete class representing Trello API Client.
"""

from os import environ

from trello import TrelloClient
from . import APIClient


class TrelloAPIClient(APIClient):
    """
    A class with the single responsibility of configuring and providing an API
    client to interact with the Trello API.
    """

    def __init__(self):
        self.initialize()

    def initialize(self):
        api_key = environ.get('TRELLO_API_KEY')
        api_secret = environ.get('TRELLO_API_TOKEN')

        if not (api_key and api_secret):
            self._client = None
        else:
            self._client = TrelloClient(
                api_key=api_key,
                api_secret=api_secret
            )

    def client(self):
        return self._client
