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
from app.services import BoardService
from app.models import Board, List
from tests.base_test_case import BaseTestCase
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


class BoardServiceTestCase(BaseTestCase):
    """Tests the `BoardService` service."""

    @patch('app.services.BoardService.__init__', new=PatchClass.boards_test_case)
    def test_fetch_inserts_boards(self):
        """
        Tests the 'fetch' method, and validates it inserts the boards into the
        database.
        """
        board_service = BoardService()

        boards = Board.query.all()
        self.assertTrue(len(boards) is 0)

        # Fetch and insert the boards into the database
        board_service.fetch()

        updated_boards = Board.query.all()
        self.assertTrue(len(updated_boards) is 2)

    @patch('app.services.BoardService.__init__', new=PatchClass.lists_test_case)
    def test_fetch_inserts_lists(self):
        """
        Tests the 'fetch' method, and validates it inserts the lists associated
        with boards into the database.
        """
        board_service = BoardService()

        boards = Board.query.all()
        lists = List.query.all()
        self.assertTrue(len(boards) is 0)
        self.assertTrue(len(lists) is 0)

        # Fetch and insert the boards and lists into the database
        board_service.fetch()

        lists = List.query.all()
        boards = Board.query.all()
        self.assertTrue(len(boards) is 2)
        self.assertTrue(len(lists) is 5)
