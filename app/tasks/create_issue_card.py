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

"""create_issue_card.py

Creates a trello card based on GitHub issue data.
"""

import textwrap
from . import CreateTrelloCard
from ..services import IssueService


class CreateIssueCard(CreateTrelloCard):
    """A class that creates a trello card on a board."""

    def __init__(self):
        """Initializes a task to create an issue trello card."""
        super().__init__()
        self._issue_service = IssueService()

    def _card_body(self):
        """Concrete helper method.

        Internal helper to format the trello card body, based on the data
        passed in.

        Returns:
            str: the markdown template for the Trello card created.
        """
        return textwrap.dedent(
            f"""
            # GitHub Issue Opened By Community Member
            ___
            - Issue link: [{self._title}]({self._url})
            - Opened by: [{self._user}]({self._user_url})
            ___
            ### Issue Body
            ___
            """
        ) + self._body

    def _persist_card_to_database(self, card):
        """Concrete helper method.

        Internal helper to save the record created to the database.

        Args:
            card (trello.Card): An object representing the Trello card created.

        Returns:
            None
        """
        self._issue_service.create(
            name=self._title,
            url=self._url,
            github_issue_id=self._id,
            repo_id=self._repo_id,
            trello_board_id=card.board_id,
            trello_card_id=card.id,
            trello_card_url=card.url,
            trello_list_id=card.list_id
        )
