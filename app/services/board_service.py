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
        fetched_boards = self.trello_service.boards()
        persisted_boards = Board.query.all()

        self._update_or_delete_boards(fetched_boards, persisted_boards)
        self._create_boards(fetched_boards, persisted_boards)

        # Persist the changes to the boards and lists
        db.session.commit()

    def _update_or_delete_boards(self, fetched_boards, persisted_boards):
        """Updates or deletes `Board` records in the database.

        Args:
            fetched_boards (list(trello.Board)): The list of boards fetched
                from the Trello API.
            persisted_boards (list(Board)): The list of persisted boards
                fetched from the database.

        Returns:
            None
        """
        fetched_board_ids = list(map(lambda x: x.id, fetched_boards))

        for record in persisted_boards:
            if record.trello_board_id in fetched_board_ids:
                # Find the trello board by unique string `trello_board_id`
                trello_board = list(
                    filter(
                        lambda x: x.id == record.trello_board_id,
                        fetched_boards
                    )
                )[0]

                # Update the attributes
                record.name = trello_board.name
                record.url = trello_board.url

                trello_lists = trello_board.all_lists()

                # Update or delete the existing lists for a given board
                self._update_or_delete_lists(trello_lists, trello_board.id)
                # Add the new lists to the database for a given board
                self._create_lists(trello_lists, trello_board.id)
            else:
                # Delete the lists that reference this board first
                persisted_lists = List.query.filter_by(board_id=record.trello_board_id)
                for l in persisted_lists:
                    db.session.delete(l)

                # Then delete this board
                db.session.delete(record)

    def _create_boards(self, fetched_boards, persisted_boards):
        """Creates records that do not exist in the database.

        Args:
            fetched_boards (list(trello.Board)): The list of boards fetched
                from the Trello API.
            persisted_boards (list(Board)): The list of persisted boards
                fetched from the database.

        Returns:
            None
        """
        persisted_board_ids = list(
            map(lambda x: x.trello_board_id, persisted_boards)
        )
        boards_to_create = list(
            filter(lambda x: x.id not in persisted_board_ids, fetched_boards)
        )

        for trello_board in boards_to_create:
            trello_board_model = Board(
                name=trello_board.name,
                url=trello_board.url,
                trello_board_id=trello_board.id
            )
            db.session.add(trello_board_model)

            # Create all the associated lists for the newly created board
            trello_lists = trello_board.all_lists()
            self._create_lists(trello_lists, trello_board.id)

    def _update_or_delete_lists(self, fetched_trello_lists, board_id):
        """Updates or deletes existing `List`s in the database.

        Args:
            fetched_trello_lists (list(trello.List)): Trello list objects to be
                updated if the `trello_list.id` matches a `trello_list_id` for
                an existing `List` record, or deleted if not.
            board_id (str): The id of the `Board` the lists are associated to.

        Returns:
            None
        """
        fetched_list_ids = list(map(lambda x: x.id, fetched_trello_lists))
        persisted_lists = List.query.filter_by(board_id=board_id)

        for record in persisted_lists:
            if record.trello_list_id in fetched_list_ids:
                # Find the trello member by unique string `trello_member_id`
                trello_list = list(
                    filter(
                        lambda x: x.id == record.trello_list_id,
                        fetched_trello_lists
                    )
                )[0]

                # Update the attributes
                record.name = trello_list.name
                record.board_id = board_id
            else:
                db.session.delete(record)

    def _create_lists(self, fetched_trello_lists, board_id):
        """Inserts new `List`s into the database.

        Args:
            fetched_trello_lists (list(trello.List)): Trello list objects to be
                inserted into the database.
            board_id (str): The id of the `Board` the lists will be associated
                to.

        Returns:
            None
        """
        persisted_lists = List.query.filter_by(board_id=board_id)
        persisted_list_ids = list(
            map(lambda x: x.trello_list_id, persisted_lists)
        )
        trello_lists_to_create = list(
            filter(
                lambda x: x.id not in persisted_list_ids,
                fetched_trello_lists
            )
        )

        for trello_list in trello_lists_to_create:
            trello_list_model = List(
                name=trello_list.name,
                trello_list_id=trello_list.id,
                board_id=board_id
            )
            db.session.add(trello_list_model)
