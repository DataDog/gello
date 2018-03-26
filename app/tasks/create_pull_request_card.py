# -*- coding: utf-8 -*-

"""create_pull_request_card.py

Creates a trello card based on GitHub pull request data.
"""

import textwrap
from . import CreateTrelloCard


class CreatePullRequestCard(CreateTrelloCard):
    """A class that creates a trello card on a board."""

    def _card_body(self):
        """Concrete helper method.

        Internal helper to format the trello card body, based on the data
        passed in.
        """
        title = self.metadata['pull_request']['title']
        url = self.metadata['pull_request']['html_url']
        body = self.metadata['pull_request']['body']
        user = self.metadata['pull_request']['user']['login']
        user_url = self.metadata['pull_request']['user']['html_url']

        return textwrap.dedent(
            f"""
            # GitHub Pull Request Opened By Community Member
            ___
            - Pull Request link: [{title}]({url})
            - Opened by: [{user}]({user_url})
            ___
            ### Pull Request Body
            ___
            """
        ) + body
