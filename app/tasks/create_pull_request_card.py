# -*- coding: utf-8 -*-

"""create_pull_request_card.py

Creates a trello card based on GitHub pull request data.
"""

import textwrap
from . import CreateTrelloCard
from ..services import PullRequestService


class CreatePullRequestCard(CreateTrelloCard):
    """A class that creates a trello card on a board."""

    def __init__(self):
        """Initializes a task to create a pull request trello card."""
        self._pull_request_service = PullRequestService()

    def _card_body(self):
        """Concrete helper method.

        Internal helper to format the trello card body, based on the data
        passed in.
        """
        self._id = self.metadata['pull_request']['id']
        self._title = self.metadata['pull_request']['title']
        self._url = self.metadata['pull_request']['html_url']
        self._body = self.metadata['pull_request']['body']
        self._user = self.metadata['pull_request']['user']['login']
        self._user_url = self.metadata['pull_request']['user']['html_url']

        return textwrap.dedent(
            f"""
            # GitHub Pull Request Opened By Community Member
            ___
            - Pull Request link: [{self._title}]({self._url})
            - Opened by: [{self._user}]({self._user_url})
            ___
            ### Pull Request Body
            ___
            """
        ) + self._body

    def _persist_card_to_database(self):
        """Concrete helper method.

        Internal helper to save the record created to the database.
        """
        self._pull_request_service.create(
            name=self._title,
            url=self._url,
            github_issue_id=self._id,
            repo_id=self._repo_id
        )
