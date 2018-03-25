# -*- coding: utf-8 -*-

"""trello_service.py

Service-helpers for interacting with the Trello API.
"""

from ..api_clients import TrelloAPIClient


class TrelloService(object):
    """
    A class with the single responsibility of interacting with the Trello API.
    """

    def __init__(self):
        """Initializes a new TrelloService object."""
        self.client = TrelloAPIClient().client()

    def boards(self):
        return self.client.list_boards()

    def create_card(self, board_id, list_id, name, desc):
        """Creates a card on a board, and a list.

        Args:
            board_id (str): The id of the board the card will be created on.
            list_id (str):  The id of the list the card will be created on.
            name (str):     The name of the card.
            desc (str):     The body of the card.

        Returns:
            None
        """
        board = self.client.get_board(board_id)
        list = board.get_list(list_id)
        list.add_card(name=name, desc=desc)
