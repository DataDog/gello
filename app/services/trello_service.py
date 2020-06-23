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
        self._client_wrapper = TrelloAPIClient()
        self.client = self._client_wrapper.client()

    def init_if_needed(self):
        if not self.client:
            self._client_wrapper.initialize()
            self.client = self._client_wrapper.client()
        return bool(self.client)

    def boards(self):
        """Returns a list of objects representing trello boards.

        Returns:
            list(trello.Board)
        """
        if self.init_if_needed():
            return self.client.list_boards()

    def members(self):
        """Returns a list of objects representing trello members.

        Returns:
            list(trello.Member)
        """
        if self.init_if_needed():
            return self._get_organization().get_members()

    def get_label_by_label_name(self, board_id, label_name):
        """Returns Trello Label with label_name from a specified board.

        Returns:
            Label
        """
        if self.init_if_needed():
            board = self.client.get_board(board_id)
            labels = board.get_labels()

            for label in labels:
                if label.name == label_name:
                    return label

            # label doesn't exist, create new label by label_name
            label_color = "red"
            new_label = board.add_label(label_name, label_color)
            assert new_label is not None
            return new_label

    def create_card(self, board_id, list_id, name, desc, label_names=[], assignee_id=None):
        """Creates a card on a board, and a list.

        Args:
            board_id (str): The id of the board the card will be created on.
            list_id (str): The id of the list the card will be created on.
            name (str): The name of the card.
            desc (str): The body of the card.
            label_names (List[str]): A list of label names.
            assignee_id (str): The trello_member_id for the card assignee.

        Returns:
            trello.Card: A card object representing a card created to a Trello
                board.
        """
        if self.init_if_needed():
            board = self.client.get_board(board_id)
            trello_list = board.get_list(list_id)

            labels = [self.get_label_by_label_name(board_id, label_name) for label_name in label_names]
            assign = [self.client.get_member(assignee_id)] if assignee_id else None

            return trello_list.add_card(name=name, desc=desc, labels=labels, assign=assign)

    def update_card_labels(self, card_id, board_id, label_names):
        new_label_names = set(label_names)

        card = self.client.get_card(card_id)
        old_labels = card.labels or []
        old_label_names = {l.name for l in old_labels}

        # Remove old labels from diff
        for label_name in old_label_names:
            if label_name not in new_label_names:
                label_to_be_removed = self.get_label_by_label_name(board_id=board_id, label_name=label_name)
                card.remove_label(label_to_be_removed)

        # Add new labels from diff
        for label_name in new_label_names:
            if label_name not in old_label_names:
                label_to_be_added = self.get_label_by_label_name(board_id=board_id, label_name=label_name)
                try:
                    # The label may have already been attached due to bulk updating to avoid concurrent update label tasks.
                    card.add_label(label_to_be_added)
                except Exception as e:
                    print("Could not add label to card", e)

    def organizations(self):
        """Returns a list of Trello organizations associated with the API Token.

        Returns:
            list(trello.Organization)
        """
        if self.init_if_needed():
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

    def _get_labels_by_board(self, board_id):
        """Returns a list of labels by board.

        Returns:
            list(dict)
        """
        return self.client.fetch_json('boards/' + board_id + '/labels')
