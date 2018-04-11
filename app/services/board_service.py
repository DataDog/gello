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

"""board_service.py

Service-helpers for creating and mutating board data.
"""

from . import APIService
from . import TrelloService
from .. import db
from ..models import Board, List


class BoardService(APIService):
    """API persistent storage service.

    A class with the single responsibility of creating/mutating Board data.
    """

    def __init__(self):
        """Initializes a new BoardService object."""
        self.trello_service = TrelloService()

    def fetch(self):
        """Creates/Updates and persists all boards and corresponding lists.

        For each of the boards fetched by the `TrelloService`, insert or update
        them, then fetch the corresponding lists and insert or update them.

        Returns:
            None
        """
        # Add all the boards to the Database for the organization
        for trello_board in self.trello_service.boards():
            self._insert_or_update_board(trello_board)

            # Add all the lists to the Database for a given board
            for trello_list in trello_board.all_lists():
                self._insert_or_update_list(trello_list, trello_board.id)

        # Persist the boards and lists
        db.session.commit()

    def _insert_or_update_board(self, board):
        """Inserts or updates the records.

        Args:
            board (trello.Board): A Trello board object to be inserted into the
                database, or updated if the `board.id` matches a
                `trello_board_id` for an existing `Board` record.

        Returns:
            None
        """
        record = Board.query.filter_by(trello_board_id=board.id).first()

        if not record:
            board_model = Board(
                name=board.name,
                url=board.url,
                trello_board_id=board.id
            )
            db.session.add(board_model)
        else:
            record.name = board.name
            record.url = board.url

    def _insert_or_update_list(self, trello_list, board_id):
        """Inserts or updates the records.

        Args:
            trello_list (trello.List): A Trello list object to be inserted into
                the database, or updated if the `trello_list.id` matches a
                `trello_list_id` for an existing `List` record.
            board_id (str): The id of the `Board` the list will be associated
                to.

        Returns:
            None
        """
        record = List.query.filter_by(trello_list_id=trello_list.id).first()

        if not record:
            list_model = List(
                name=trello_list.name,
                trello_list_id=trello_list.id,
                board_id=board_id
            )
            db.session.add(list_model)
        else:
            record.name = trello_list.name
            record.board_id = board_id
