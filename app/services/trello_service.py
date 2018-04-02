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

"""trello_service.py

Service-helpers for interacting with the Trello API.
"""

from os import environ
from ..api_clients import TrelloAPIClient


class TrelloService(object):
    """
    A class with the single responsibility of interacting with the Trello API.
    """

    def __init__(self):
        """Initializes a new TrelloService object."""
        self.client = TrelloAPIClient().client()
        self.organization = self._get_organization()

    def boards(self):
        """Returns a list of objects representing trello boards."""
        return self.client.list_boards()

    def members(self):
        """Returns a list of objects representing trello members."""
        return self.organization.get_members()

    def create_card(self, board_id, list_id, name, desc):
        """Creates a card on a board, and a list.

        Args:
            board_id (str): The id of the board the card will be created on.
            list_id (str):  The id of the list the card will be created on.
            name (str):     The name of the card.
            desc (str):     The body of the card.

        Returns:
            Card
        """
        board = self.client.get_board(board_id)
        list = board.get_list(list_id)
        return list.add_card(name=name, desc=desc)

    def delete_card(self, card_id):
        """Deletes a card for a given `card_id`."""
        self.client.get_card(card_id=card_id).delete()

    def _get_organization(self):
        """XXX: handle error case where the organization does not exist"""
        orgs = self.client.list_organizations()
        return next(
            o for o in orgs if o.name == environ.get('TRELLO_ORG_NAME')
        )
