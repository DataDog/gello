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

import json
from app import db
from mock import patch
from app.models import PullRequest
from app.tasks import CreatePullRequestCard
from tests.utils import create_board, create_repo, create_list, \
    create_subscription, create_subscribed_list, default_board_id, \
    default_list_id, mock_trello_service
from tests.base_test_case import BaseTestCase


class PatchClass:
    """A class used to patch the `CreatePullRequestCard` constructor."""

    def __init__(self):
        self.trello_service = mock_trello_service(
            board_count=0,
            list_counts=[]
        )


class CreatePullRequestCardTestCase(BaseTestCase):
    """Tests the `CreatePullRequestCard` celery task."""

    def setUp(self):
        """Sets up testing context."""
        super().setUp()
        create_board()
        create_repo()
        create_list()
        create_subscription()
        create_subscribed_list()
        db.session.commit()

    @patch('app.tasks.CreatePullRequestCard.trello_service')
    def test_run(self, mock):
        """Tests to ensure a new `PullRequest` is persisted when run."""
        mock.return_value = mock_trello_service()

        pull_requests = PullRequest.query.all()
        self.assertTrue(len(pull_requests) is 0)

        payload = json.loads(open('./tests/fixtures/pull_request_opened.json').read())
        CreatePullRequestCard.delay(
            board_id=default_board_id,
            list_id=default_list_id,
            name='Fake Pull Request',
            payload=payload
        )

        # Enqueuing new pull_request `CreatePullRequestCard` should create a
        # `PullRequest` record
        new_pull_requests = PullRequest.query.all()
        self.assertTrue(len(new_pull_requests) is 1)
