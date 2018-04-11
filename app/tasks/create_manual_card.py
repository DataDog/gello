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

"""create_manual_card.py

Creates a trello card based on GitHub manual data.
"""

import textwrap
from . import CreateTrelloCard
from ..services import IssueService, PullRequestService


class CreateManualCard(CreateTrelloCard):
    """A class that creates a trello card on a board."""

    def __init__(self):
        """Initializes a task to create a manual trello card."""
        self._issue_service = IssueService()
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
            # GitHub Card Opened By Organization Member
            ___
            - Link: [{self._title}]({self._url})
            - Opened by: [{self._user}]({self._user_url})
            ___
            ### {self.get_scope().capitalize()} Body
            ___
            """
        ) + self._body

    def _persist_card_to_database(self, card):
        """Concrete helper method.

        Internal helper to save the record created to the database.

        Args:
            card (trello.Card): an object representing the trello card created

        Returns:
            None
        """
        scope = self.get_scope()

        if scope == 'issue':
            self._issue_service.create(
                name=self._title,
                url=self._url,
                github_issue_id=self._id,
                repo_id=self._repo_id,
                trello_board_id=card.board_id,
                trello_card_id=card.id,
                trello_card_url=card.url
            )
        elif scope == 'pull_request':
            self._pull_request_service.create(
                name=self._title,
                url=self._url,
                github_pull_request_id=self._id,
                repo_id=self._repo_id,
                trello_board_id=card.board_id,
                trello_card_id=card.id,
                trello_card_url=card.url
            )
        else:
            print('Unsupported GitHub scope')
