# -*- coding: utf-8 -*-

"""create_issue_card.py

Creates a trello card based on GitHub issue data.
"""

import textwrap
from . import CreateTrelloCard


class CreateIssueCard(CreateTrelloCard):
    """A class that creates a trello card on a board."""

    def _card_body(self):
        """Concrete helper method.

        Internal helper to format the trello card body, based on the data
        passed in.
        """
        title = self.metadata['issue']['title']
        url = self.metadata['issue']['html_url']
        body = self.metadata['issue']['body']
        user = self.metadata['issue']['user']['login']
        user_url = self.metadata['issue']['user']['html_url']

        return textwrap.dedent(
            f"""
            # GitHub Issue Opened By Community Member
            ___
            - Issue link: [{title}]({url})
            - Opened by: [{user}]({user_url})
            ___
            ### Issue Body
            ___
            {body}
            """
        )
