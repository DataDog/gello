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

    def boards(self):
        """Returns a list of objects representing trello boards.

        Returns:
            list(trello.Board)
        """
        return self.client.list_boards()

    def members(self):
        """Returns a list of objects representing trello members.

        Returns:
            list(trello.Member)
        """
        return self._get_organization().get_members()

    def create_card(self, board_id, list_id, name, desc, assignee_id=None):
        """Creates a card on a board, and a list.

        Args:
            board_id (str): The id of the board the card will be created on.
            list_id (str): The id of the list the card will be created on.
            name (str): The name of the card.
            desc (str): The body of the card.
            assignee_id (str): The trello_member_id for the card assignee

        Returns:
            trello.Card: A card object representing a card created to a Trello
                board.
        """
        board = self.client.get_board(board_id)
        trello_list = board.get_list(list_id)
        asign = [self.client.get_member(assignee_id)] if assignee_id else None

        return trello_list.add_card(name=name, desc=desc, assign=asign)

    def organizations(self):
        """Returns a list of Trello organizations associated with the API Token.

        Returns:
            list(trello.Organization)
        """
        return self.client.list_organizations()

    def _get_organization(self):
        """Returns a representation of the Trello organization.

        Returns:
            trello.Organization
        """
        if 'TRELLO_ORG_NAME' not in environ:
            print('Must supply the `TRELLO_ORG_NAME` variable.')
            return

        orgs = self.organizations()
        return next(
            o for o in orgs if o.name == environ.get('TRELLO_ORG_NAME')
        )
