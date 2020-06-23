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

"""update_pull_request_card_labels.py

Updates a trello card labels based on GitHub pull request data.
"""

import textwrap
from . import GitHubBaseTask
from ..services import TrelloService
from ..models import PullRequest


class UpdatePullRequestCardLabels(GitHubBaseTask):
    """A class that updates the labels of a trello card on a board."""

    def __init__(self):
        """Initializes a task to update the labels of a issue trello card."""
        self._trello_service = TrelloService()

    def run(self, pull_request_id, board_id, label_names, payload):
        """Performs validations on the event type and enqueues them.

        Validates the event being received is a GitHub Pull Request event or a
        GitHub Issue event, and then enqueues it in the corresponding events
        queue.

        Args:
            pull_request_id (str): The id of the Github pull request.
            board_id (str): The id of the board the card will be created on.
            label_names (List[str]): A list of label names.
            payload (dict): Github data specific to the Trello card to be updated.

        Returns:
            None
        """
        self.payload = payload
        self.set_scope_data()
        pull_request = PullRequest.query.filter_by(trello_board_id=board_id, github_pull_request_id=pull_request_id).first()
        self._trello_service.update_card_labels(pull_request.trello_card_id, board_id, label_names)
