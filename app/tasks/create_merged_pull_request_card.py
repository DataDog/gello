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

"""create_pull_request_card.py

Creates a trello card based on GitHub pull request data.
"""

import textwrap
from . import CreateTrelloCard
from ..services import PullRequestService


class CreateMergedPullRequestCard(CreateTrelloCard):
    """A class that creates a trello card on a board."""

    def __init__(self):
        """Initializes a task to create a merged pull request trello card."""
        super().__init__()
        self._pull_request_service = PullRequestService()

    def _card_body(self):
        """Concrete helper method.

        Internal helper to format the trello card body, based on the data
        passed in.

        Returns:
            str: the markdown template for the Trello card created.
        """
        return textwrap.dedent(
            f"""
            # GitHub Pull Request Merged
            ___
            - Pull Request link: [{self._title}]({self._url})
            - Opened by: [{self._user}]({self._user_url})
            ___
            ### Pull Request Body
            ___
            """
        ) + self._body

    def _persist_card_to_database(self, card):
        """Concrete helper method.

        Internal helper to save the record created to the database.

        Args:
            card (trello.Card): An object representing the trello card created.

        Returns:
            None
        """
        self._pull_request_service.create(
            name=self._title,
            url=self._url,
            github_pull_request_id=self._id,
            repo_id=self._repo_id,
            trello_board_id=card.board_id,
            trello_card_id=card.id,
            trello_card_url=card.url
        )
