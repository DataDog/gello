# -*- coding: utf-8 -*-

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
        self._client = TrelloClient(
            api_key=environ.get('TRELLO_API_KEY'),
            api_secret=environ.get('TRELLO_API_TOKEN')
        )

    def client(self):
        return self._client
