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
from app import db
from app.services import IssueService
from app.models import Issue
from tests.base_test_case import BaseTestCase
from tests.utils import create_repo, default_repo_id


class IssueServiceTestCase(BaseTestCase):
    """Tests the `IssueService` service."""

    # The `github_issue_id` for the `Issue` tested
    issue_id = 100000
    issue_name = 'some issue'
    repo_id = 100001

    def setUp(self):
        """Sets up testing context."""
        super().setUp()
        self.issue_service = IssueService()
        create_repo()
        db.session.commit()

    def test_create(self):
        """Test that an issue is successfully created."""
        board_id = uuid.uuid1()

        issues = Issue.query.all()
        self.assertTrue(len(issues) is 0)

        # Create the issue
        self.issue_service.create(
            name=self.issue_name,
            url='https://github.com/user/repo/issues/1',
            github_issue_id=self.issue_id,
            repo_id=default_repo_id,
            trello_board_id=board_id,
            trello_card_id=uuid.uuid1(),
            trello_card_url=f"https://trello.com/c/{board_id}/a-card"
        )

        new_issues = Issue.query.all()
        self.assertTrue(len(new_issues) is 1)

    def test_update(self):
        """Test that an `Issue` is successfully updated."""
        self.test_create()

        issue = Issue.query.filter_by(github_issue_id=self.issue_id).first()
        self.assertTrue(issue.name == self.issue_name)

        new_issue_name = 'some new issue name'
        self.issue_service.update(
            github_issue_id=self.issue_id,
            name=new_issue_name
        )

        new_issue = Issue.query.filter_by(github_issue_id=self.issue_id).first()
        self.assertTrue(new_issue.name == new_issue_name)

    def test_delete(self):
        """Test that an issue is successfully deleted."""
        self.test_create()

        issues = Issue.query.all()
        self.assertTrue(len(issues) is 1)

        # Delete the issue
        self.issue_service.delete(github_issue_id=self.issue_id)

        new_issues = Issue.query.all()
        self.assertTrue(len(new_issues) is 0)
