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
        """
        scope = self._get_scope()
        self._id = self.metadata[scope]['id']
        self._title = self.metadata[scope]['title']
        self._url = self.metadata[scope]['html_url']
        self._body = self.metadata[scope]['body']
        self._user = self.metadata[scope]['user']['login']
        self._user_url = self.metadata[scope]['user']['html_url']

        return textwrap.dedent(
            f"""
            # GitHub Card Opened By Organization Member
            ___
            - Link: [{self._title}]({self._url})
            - Opened by: [{self._user}]({self._user_url})
            ___
            ### {scope.capitalize()} Body
            ___
            """
        ) + self._body

    def _persist_card_to_database(self):
        """Concrete helper method.

        Internal helper to save the record created to the database.
        """
        pass

    def _get_scope(self):
        """Returns the scope of the payload (i.e., issue, pull_request)."""

        if 'issue' in self.metadata:
            return 'issue'
        elif 'pull_request' in self.metadata:
            return 'pull_request'
        else:
            print('Unsupported event action.')
