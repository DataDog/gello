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

from mock import patch
from unittest import TestCase

from app import create_app, db
from app.services import BoardService
from app.models import Board, List
from tests.utils import mock_trello_service


class PatchClass:
    """A class used to patch the `BoardService` constructor."""

    def boards_test_case(self):
        self.trello_service = mock_trello_service(
            board_count=2,
            list_counts=[0, 0]
        )

    def lists_test_case(self):
        self.trello_service = mock_trello_service(
            board_count=2,
            list_counts=[2, 3]
        )


class BoardServiceTestCase(TestCase):
    """Tests the `BoardService` service."""

    def setUp(self):
        # Prepare application
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Prepare database
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @patch('app.services.BoardService.__init__', new=PatchClass.boards_test_case)
    def test_fetch_inserts_boards(self):
        """
        Tests the 'fetch' method, and validates it inserts the boards into the
        database.
        """
        board_service = BoardService()

        boards = Board.query.all()
        self.assertTrue(boards.count() is 0)

        # Fetch and insert the boards into the database
        board_service.fetch()

        updated_boards = Board.query.all()
        self.assertTrue(updated_boards.count() is 2)

    @patch('app.services.BoardService.__init__', new=PatchClass.lists_test_case)
    def test_fetch_inserts_lists(self):
        """
        Tests the 'fetch' method, and validates it inserts the lists associated
        with boards into the database.
        """
        boards = Board.query.all()
        lists = List.query.all()
        self.assertTrue(boards.count() is 0)
        self.assertTrue(lists.count() is 0)

        # Fetch and insert the boards and lists into the database
        self.board_service.fetch()

        lists = List.query.all()
        boards = Board.query.all()
        self.assertTrue(boards.count() is 2)
        self.assertTrue(lists.count() is 5)
