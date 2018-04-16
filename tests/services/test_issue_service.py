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

import uuid
from unittest import TestCase

from app import create_app, db
from app.services import IssueService
from app.models import Issue, Repo


class IssueServiceTestCase(TestCase):
    """Tests the `IssueService` service."""

    # The `github_issue_id` for the `Issue` tested
    issue_id = 100000
    repo_id = 100001

    def setUp(self):
        """Sets up testing context."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Prepare database
        db.create_all()

        self.issue_service = IssueService()

        # Create the repo needed for the foreign key constraint
        db.session.add(
            Repo(
                name='repo_name',
                url='https://github.com/user/repo',
                github_repo_id=self.repo_id
            )
        )
        db.session.commit()

    def tearDown(self):
        """Tears down testing context."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create(self):
        """Test that an issue is successfully created."""
        issue_name = 'some issue'
        board_id = uuid.uuid1()

        issues = Issue.query.all()
        self.assertTrue(len(issues) is 0)

        # Create the issue
        self.issue_service.create(
            name=issue_name,
            url='https://github.com/user/repo/issues/1',
            github_issue_id=self.issue_id,
            repo_id=self.repo_id,
            trello_board_id=board_id,
            trello_card_id=uuid.uuid1(),
            trello_card_url=f"https://trello.com/c/{board_id}/a-card"
        )

        new_issues = Issue.query.all()
        self.assertTrue(len(new_issues) is 1)

    def test_delete(self):
        """Test that an issue is successfully deleted."""
        self.test_create()

        issues = Issue.query.all()
        self.assertTrue(len(issues) is 1)

        # Delete the issue
        self.issue_service.delete(github_issue_id=self.issue_id)

        new_issues = Issue.query.all()
        self.assertTrue(len(new_issues) is 0)
