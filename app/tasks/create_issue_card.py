# -*- coding: utf-8 -*-

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
        self._issue_service = IssueService()

    def _card_body(self):
        """Concrete helper method.

        Internal helper to format the trello card body, based on the data
        passed in.
        """
        self._id = self.metadata['issue']['id']
        self._title = self.metadata['issue']['title']
        self._url = self.metadata['issue']['html_url']
        self._body = self.metadata['issue']['body']
        self._user = self.metadata['issue']['user']['login']
        self._user_url = self.metadata['issue']['user']['html_url']

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

    def _persist_card_to_database(self):
        """Concrete helper method.

        Internal helper to save the record created to the database.
        """
        self._issue_service.create(
            name=self._title,
            url=self._url,
            github_issue_id=self._id,
            repo_id=self._repo_id
        )
