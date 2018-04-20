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
from app.services import PullRequestService
from app.models import PullRequest, Repo
from tests.base_test_case import BaseTestCase


class PullRequestServiceTestCase(BaseTestCase):
    """Tests the `PullRequestService` service."""

    # The `github_pull_request_id` for the `PullRequest` tested
    pull_request_id = 100000
    repo_id = 100001

    def setUp(self):
        """Sets up testing context."""
        super().setUp()
        self.pull_request_service = PullRequestService()

        # Create the repo needed for the foreign key constraint
        db.session.add(
            Repo(
                name='repo_name',
                url='https://github.com/user/repo',
                github_repo_id=self.repo_id
            )
        )
        db.session.commit()

    def test_create(self):
        """Test that a pull request is successfully created."""
        pull_request_name = 'some pull_request'
        board_id = uuid.uuid1()

        pull_requests = PullRequest.query.all()
        self.assertTrue(len(pull_requests) is 0)

        # Create the pull_request
        self.pull_request_service.create(
            name=pull_request_name,
            url='https://github.com/user/repo/pulls/1',
            github_pull_request_id=self.pull_request_id,
            repo_id=self.repo_id,
            trello_board_id=board_id,
            trello_card_id=uuid.uuid1(),
            trello_card_url=f"https://trello.com/c/{board_id}/a-card"
        )

        new_pull_requests = PullRequest.query.all()
        self.assertTrue(len(new_pull_requests) is 1)

    def test_delete(self):
        """Test that a pull request is successfully deleted."""
        self.test_create()

        pull_requests = PullRequest.query.all()
        self.assertTrue(len(pull_requests) is 1)

        # Delete the pull_request
        self.pull_request_service.delete(
            github_pull_request_id=self.pull_request_id
        )

        new_pull_requests = PullRequest.query.all()
        self.assertTrue(len(new_pull_requests) is 0)
