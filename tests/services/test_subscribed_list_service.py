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
from app.services import SubscribedListService
from app.models import SubscribedList
from tests.base_test_case import BaseTestCase
from tests.utils import create_board, create_repo, create_list, \
    create_subscription, default_board_id, default_repo_id, default_list_id


class SubscribedListServiceTestCase(BaseTestCase):
    """Tests the `SubscribedListService` service."""

    def setUp(self):
        """Sets up testing context."""
        super().setUp()
        self.subscribed_list_service = SubscribedListService()
        create_board()
        create_repo()
        create_list()
        create_subscription()
        db.session.commit()

    def test_create(self):
        """Test that an subscribed_list is successfully created."""
        subscribed_lists = SubscribedList.query.all()
        self.assertTrue(len(subscribed_lists) is 0)

        # Create the subscribed_list
        self.subscribed_list_service.create(
            board_id=default_board_id,
            repo_id=default_repo_id,
            list_id=default_list_id,
        )

        new_subscribed_lists = SubscribedList.query.all()
        self.assertTrue(len(new_subscribed_lists) is 1)

    def test_update(self):
        """Test that a subscribed_list is successfully updated."""
        self.test_create()

        primary_key = [default_board_id, default_repo_id, default_list_id]

        subscribed_list = SubscribedList.query.get(primary_key)
        self.assertTrue(subscribed_list.trello_member_id is None)

        new_member_id = 'new_member_uuid'
        self.subscribed_list_service.update(
            board_id=default_board_id,
            repo_id=default_repo_id,
            list_id=default_list_id,
            trello_member_id=new_member_id
        )

        updated_list = SubscribedList.query.get(primary_key)
        self.assertTrue(updated_list.trello_member_id == new_member_id)

    def test_delete(self):
        """Test that an subscribed_list is successfully deleted."""
        self.test_create()

        subscribed_lists = SubscribedList.query.all()
        self.assertTrue(len(subscribed_lists) is 1)

        # Delete the subscribed_list
        self.subscribed_list_service.delete(
            board_id=default_board_id,
            repo_id=default_repo_id,
            list_id=default_list_id
        )

        new_subscribed_lists = SubscribedList.query.all()
        self.assertTrue(len(new_subscribed_lists) is 0)
