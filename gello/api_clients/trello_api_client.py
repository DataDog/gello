# -*- coding: utf-8 -*-

"""Concrete class representing
"""

from os import environ
from trello import TrelloClient
from gello.api_clients import APIClient
from gello.utils.decorators import memoized


class TrelloAPIClient(APIClient):
    """
    A class with the single responsibility of configuring and providing an API
    client to interact with the Trello API.
    """

    @memoized
    def client(self):
        """
        @return
        """
        return TrelloClient(
            api_key=environ.get('TRELLO_API_KEY'),
            api_secret=environ.get('TRELLO_API_SECRET'),
            token=environ.get('TRELLO_API_TOKEN'),
            token_secret=environ.get('TRELLO_API_SECRET')
        )
