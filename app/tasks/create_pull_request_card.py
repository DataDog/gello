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
        return textwrap.dedent(
            f"""
            ### GitHub Pull Request - {self.metadata['name']}
            """
        )
