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
from app.services import TrelloSubscriptionService
from app.models import Subscription
from tests.base_test_case import BaseTestCase
from tests.utils import create_board, create_repo, default_board_id, \
    default_repo_id


class SubscriptionServiceTestCase(BaseTestCase):
    """Tests the `SubscriptionService` service."""

    def setUp(self):
        """Sets up testing context."""
        super().setUp()
        self.subscription_service = TrelloSubscriptionService()
        create_board()
        create_repo()
        db.session.commit()

    def test_create(self):
        """Test that an subscription is successfully created."""
        subscriptions = Subscription.query.all()
        self.assertTrue(len(subscriptions) is 0)

        # Create the subscription
        self.subscription_service.create(
            board_id=default_board_id,
            repo_id=default_repo_id,
            issue_autocard=True,
            pull_request_autocard=True
        )

        new_subscriptions = Subscription.query.all()
        self.assertTrue(len(new_subscriptions) is 1)

    def test_update(self):
        """Test that a subscription is successfully updated."""
        self.test_create()

        subscription = Subscription.query.filter_by(board_id=default_board_id,
                                                    repo_id=default_repo_id
                                                    ).first()

        primary_key = [subscription.id, default_repo_id]

        self.assertTrue(subscription.issue_autocard)

        self.subscription_service.update(
            board_id=default_board_id,
            repo_id=default_repo_id,
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
            board_id=default_board_id,
            repo_id=default_repo_id
        )

        new_subscriptions = Subscription.query.all()
        self.assertTrue(len(new_subscriptions) is 0)
