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
from app.models import Issue
from app.tasks import CreateIssueCard
from tests.utils import create_board, create_repo, create_list, \
    create_subscription, create_subscribed_list, default_board_id, \
    default_list_id, mock_trello_service
from tests.base_test_case import BaseTestCase


class CreateIssueCardTestCase(BaseTestCase):
    """Tests the `CreateIssueCard` celery task."""

    def setUp(self):
        """Sets up testing context."""
        super().setUp()
        create_board()
        create_repo()
        create_list()
        create_subscription()
        create_subscribed_list()
        db.session.commit()

    @patch('app.tasks.CreateIssueCard.trello_service')
    def test_run(self, mock):
        """Tests to ensure a new `Issue` is persisted when the task is run."""
        mock.return_value = mock_trello_service()

        issues = Issue.query.all()
        self.assertTrue(len(issues) is 0)

        payload = json.loads(open('./tests/fixtures/issue_opened.json').read())
        CreateIssueCard.delay(
            board_id=default_board_id,
            list_id=default_list_id,
            name='Fake Issue',
            payload=payload
        )

        # Enqueuing new issue `CreateIssueCard` should create an `Issue` record
        new_issues = Issue.query.all()
        self.assertTrue(len(new_issues) is 1)
