# -*- coding: utf-8 -*-

"""create_trello_card.py

Creates a card with a name and body on a given Trello board.
"""

from celery.task import Task


class CreateTrelloCard(Task):
    """A class that creates a trello card on a board."""

    def run(self, card_name, board):
        """Performs validations on the event type and enqueues them.

        Validates the event being received is a GitHub Pull Request event or a
        GitHub Issue event, and then enqueues it in the corresponding events
        queue.
        """
        print(f"Creating trello card {card_name} on {board}")
        self.card_name = card_name
        self.board = board

    def _format_card_body(self):
        """Helper method.

        Internal helper to format the trello card body, based on the data passed
        in.
        """
        pass
