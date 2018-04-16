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
from app.services import SubscriptionService
from app.models import Board, Repo, Subscription


class SubscriptionServiceTestCase(TestCase):
    """Tests the `SubscriptionService` service."""

    board_id = str(uuid.uuid1())
    repo_id = 100001

    def setUp(self):
        """Sets up testing context."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Prepare database
        db.create_all()

        self.subscription_service = SubscriptionService()

        # Create the board needed for the foreign key constraint
        db.session.add(
            Board(
                name='board_name',
                url=f"https://trello.com/c/{self.board_id}/a-card",
                trello_board_id=self.board_id
            )
        )

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
        """Test that an subscription is successfully created."""
        subscriptions = Subscription.query.all()
        self.assertTrue(len(subscriptions) is 0)

        # Create the subscription
        self.subscription_service.create(
            board_id=self.board_id,
            repo_id=self.repo_id,
            issue_autocard=True,
            pull_request_autocard=True
        )

        new_subscriptions = Subscription.query.all()
        self.assertTrue(len(new_subscriptions) is 1)

    def test_update(self):
        """Test that a subscription is successfully updated."""
        self.test_create()

        primary_key = [self.board_id, self.repo_id]

        subscription = Subscription.query.get(primary_key)
        self.assertTrue(subscription.issue_autocard)

        self.subscription_service.update(
            board_id=self.board_id,
            repo_id=self.repo_id,
            issue_autocard=False,
            pull_request_autocard=True
        )

        updated_subscription = Subscription.query.get(primary_key)
        self.assertFalse(updated_subscription.issue_autocard)

    def test_delete(self):
        """Test that an subscription is successfully deleted."""
        self.test_create()

        subscriptions = Subscription.query.all()
        self.assertTrue(len(subscriptions) is 1)

        # Delete the subscription
        self.subscription_service.delete(
            board_id=self.board_id,
            repo_id=self.repo_id
        )

        new_subscriptions = Subscription.query.all()
        self.assertTrue(len(new_subscriptions) is 0)
