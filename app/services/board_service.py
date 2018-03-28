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

from . import TrelloService
from .. import db
from ..models import Board, List


class BoardService(object):
    """CRUD persistent storage service.

    A class with the single responsibility of creating/mutating Board data.
    """

    def __init__(self):
        """Initializes a new BoardService object."""
        self.trello_service = TrelloService()

    def create_or_update_boards(self):
        """Creates/Updates and persists all boards and corresponding lists."""
        # Add all the boards to the Database for the organization
        for trello_board in self.trello_service.boards():
            board = Board(
                name=trello_board.name,
                url=trello_board.url,
                trello_board_id=trello_board.id
            )
            db.session.add(board)

            # Add all the lists to the Database for a given board
            for trello_list in trello_board.all_lists():
                list_model = List(
                    active=False,
                    name=trello_list.name,
                    trello_list_id=trello_list.id,
                    board_id=trello_board.id
                )
                db.session.add(list_model)

        # Persist the boards and lists
        db.session.commit()
