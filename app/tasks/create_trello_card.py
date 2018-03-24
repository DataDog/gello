# -*- coding: utf-8 -*-

"""create_trello_card.py

Creates a card with a name and body on a given Trello board.
"""

from celery.task import Task
from ..services import TrelloService


class CreateTrelloCard(Task):
    """An abstract class that creates a trello card on a board."""

    def run(self, board_id: str, list_id: str, name: str, metadata: dict):
        """Performs validations on the event type and enqueues them.

        Validates the event being received is a GitHub Pull Request event or a
        GitHub Issue event, and then enqueues it in the corresponding events
        queue.

        Args:
            board_id (str):  The id of the board the card will be created on.
            list_id (str):   The id of the list the card will be created on.
            name (str):      The name of the card.
            metadata (dict): The card-specific data, used in the `_card_body`
                             template method.

        Returns:
            None
        """
        self.metadata = metadata
        self.board_id = board_id

        TrelloService().create_card(
            board_id=board_id,
            list_id=list_id,
            name=name,
            desc=self._card_body()
        )

    def _card_body(self):
        """Abstract helper method.

        Internal helper to format the trello card body, based on the data
        passed in.
        """
        pass
