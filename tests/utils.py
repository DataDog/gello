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

"""utils.py

Testing utils for stubbing classes and methods
"""

import uuid
import mock


def make_board(board_num, list_count):
    """Creates a board with a new name each time the function is called."""
    board_id = str(uuid.uuid1())
    board = mock.MagicMock(
        id=board_id,
        url=f"https://trello.com/b/{board_id}",
        return_value=None
    )
    board.name = f"board_{board_num}",
    board.all_lists.return_value = [
        make_list(board_id, i) for i in range(list_count)
    ]

    return board


def make_list(board_id, list_num):
    """Creates a list with a new name each time the function is called."""
    trello_list = mock.MagicMock(
        board_id=board_id,
        id=str(uuid.uuid1()),
        return_value=None
    )
    trello_list.name = f"list_{list_num}",

    return trello_list


def mock_trello_service(board_count, list_counts=[]):
    """Stubs out the TrelloService for testing purposes."""
    assert(board_count is len(list_counts))

    trello_service = mock.MagicMock()
    trello_service.boards.return_value = [
        make_board(i, list_counts[i]) for i in range(board_count)
    ]

    return trello_service
