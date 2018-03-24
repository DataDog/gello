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
        return textwrap.dedent(
            """
            ### [GitHub Issue]({self.metadata['url']})
            """
        )
