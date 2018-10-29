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

"""create_trello_card.py

Creates a card with a name and body on a given Trello board.
"""

from . import GitHubBaseTask
from ..services import TrelloService


class CreateTrelloCard(GitHubBaseTask):
    """An abstract class that creates a trello card on a board."""

    def __init__(self):
        """Initializes a task to create a trello card."""
        self._trello_service = TrelloService()

    def run(self, board_id, list_id, name, payload, assignee_id=None):
        """Performs validations on the event type and enqueues them.

        Validates the event being received is a GitHub Pull Request event or a
        GitHub Issue event, and then enqueues it in the corresponding events
        queue.

        Args:
            board_id (str): The id of the board the card will be created on.
            list_id (str): The id of the list the card will be created on.
            name (str): The name of the card.
            payload (dict): The card-specific data, used in the `_card_body`
                template method.
            assignee_id (str): The trello_member_id for the card assignee.

        Returns:
            None
        """
        self.payload = payload
        self.set_scope_data()
        self._repo_id = self.payload['repository']['id']

        # Create a trello card on a given board, and list
        card = self.trello_service().create_card(
            board_id=board_id,
            list_id=list_id,
            name=name,
            desc=self._card_body(),
            assignee_id=assignee_id
        )
        card.attach(self._title, url=self._url)

        # Persist the card object to the database
        self._persist_card_to_database(card=card)

    def trello_service(self):
        """Reutrns the TrelloService instance.

        Returns:
            TrelloService
        """
        return self._trello_service

    def _card_body(self):
        """Abstract helper method.

        Internal helper to format the Trello card body, based on the data
        passed in.
        """
        pass

    def _persist_card_to_database(self, card):
        """Abstract helper method.

        Internal helper to save the record created to the database.
        """
        pass
