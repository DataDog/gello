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

"""create_trello_webhook_for_boards.py

Creates a webhook for a Trello model.
"""

from celery.task import Task
from .. import db
from ..models import Board
from ..services import TrelloService


class CreateTrelloWebhooksForBoards(Task):
    """A task to create a Trello webhook."""

    def __init__(self):
        """Initializes a `TrelloService` object for the class."""
        self._trello_service = TrelloService()

    def run(self, url_root):
        """Creates a Trello webhook for all `trello.Board` models.

        Args:
            url_root (str): The root url for Gello.

        Returns:
            None
        """
        boards = Board.query.filter_by(webhooks_active=True)

        for trello_board in boards:
            webhook_created = self._trello_service.create_webhook(
                url_root=url_root,
                trello_model_id=trello_board.trello_board_id
            )

            if webhook_created:
                trello_board.webhooks_active = True

        # Persist the changes
        db.session.commit()
