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

from app import db
from app.models import Issue, PullRequest
from app.tasks import DeleteCardObjectFromDatabase
from tests.utils import create_board, create_repo, create_list, \
    create_subscription, create_subscribed_list, create_issue, \
    default_issue_id, create_pull_request, default_pull_request_id
from tests.base_test_case import BaseTestCase


class DeleteCardObjectFromDatabaseTestCase(BaseTestCase):
    """Tests the `DeleteCardObjectFromDatabase` celery task."""

    def setUp(self):
        """Sets up testing context."""
        super().setUp()
        create_board()
        create_repo()
        create_list()
        create_subscription()
        create_subscribed_list()
        db.session.commit()

    def test_deleting_issue(self):
        """Tests to ensure a `Issue` is deleted when the task is run."""
        create_issue()

        issues = Issue.query.all()
        self.assertTrue(len(issues) is 1)

        DeleteCardObjectFromDatabase.delay(
            scope='issue',
            github_id=default_issue_id
        )

        # Enqueuing new `DeleteCardObjectFromDatabase` task should delete the
        # corresponding `Issue` record
        new_issues = Issue.query.all()
        self.assertTrue(len(new_issues) is 0)

    def test_deleting_pull_request(self):
        """Tests to ensure a `PullRequest` is deleted the task is run."""
        create_pull_request()

        pull_requests = PullRequest.query.all()
        self.assertTrue(len(pull_requests) is 1)

        DeleteCardObjectFromDatabase.delay(
            scope='pull_request',
            github_id=default_pull_request_id
        )

        # Enqueuing new `DeleteCardObjectFromDatabase` task should delete the
        # corresponding `PullRequest` record
        new_pull_requests = PullRequest.query.all()
        self.assertTrue(len(new_pull_requests) is 0)
