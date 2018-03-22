# -*- coding: utf-8 -*-

"""TrelloService
"""

from ..api_clients import TrelloAPIClient


class TrelloService(object):
    """
    A class with the single responsibility of interacting with the Trello API
    """

    def __init__(self):
        """Initializes a new TrelloService object."""
        self.api_client = TrelloAPIClient()

    def boards(self):
        pass
