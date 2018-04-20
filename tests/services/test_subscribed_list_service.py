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
from app.services import SubscribedListService
from app.models import Board, List, Repo, Subscription, SubscribedList
from tests.base_test_case import BaseTestCase


class SubscribedListServiceTestCase(BaseTestCase):
    """Tests the `SubscribedListService` service."""

    board_id = str(uuid.uuid1())
    list_id = str(uuid.uuid1())
    repo_id = 100001

    def setUp(self):
        """Sets up testing context."""
        super().setUp()
        self.subscribed_list_service = SubscribedListService()

        # Create the board needed for the foreign key constraint
        db.session.add(
            Board(
                name='board_name',
                url=f"https://trello.com/c/{self.board_id}/a-card",
                trello_board_id=self.board_id
            )
        )

        # Create the list needed for the foreign key constraint
        db.session.add(
            List(
                name='list_name',
                trello_list_id=self.list_id,
                board_id=self.board_id
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

        # Create the subscription needed for the foreign key constraint
        db.session.add(
            Subscription(board_id=self.board_id, repo_id=self.repo_id)
        )

        db.session.commit()

    def test_create(self):
        """Test that an subscribed_list is successfully created."""
        subscribed_lists = SubscribedList.query.all()
        self.assertTrue(len(subscribed_lists) is 0)

        # Create the subscribed_list
        self.subscribed_list_service.create(
            board_id=self.board_id,
            repo_id=self.repo_id,
            list_id=self.list_id,
        )

        new_subscribed_lists = SubscribedList.query.all()
        self.assertTrue(len(new_subscribed_lists) is 1)

    def test_update(self):
        """Test that a subscribed_list is successfully updated."""
        self.test_create()

        primary_key = [self.board_id, self.repo_id, self.list_id]

        subscribed_list = SubscribedList.query.get(primary_key)
        self.assertTrue(subscribed_list.trello_member_id is None)

        new_member_id = 'new_member_uuid'
        self.subscribed_list_service.update(
            board_id=self.board_id,
            repo_id=self.repo_id,
            list_id=self.list_id,
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
            board_id=self.board_id,
            repo_id=self.repo_id,
            list_id=self.list_id
        )

        new_subscribed_lists = SubscribedList.query.all()
        self.assertTrue(len(new_subscribed_lists) is 0)
