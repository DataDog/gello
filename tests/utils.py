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
import trello
import mock


def make_organization():
    """Stubs out a trello organization."""
    organization = mock.MagicMock(
        organization_id='some_org_id',
        name='some_org'
    )
    organization.client = mock.MagicMock()
    return organization


def make_board(board_id, list_count):
    """Creates a board with a new name each time the function is called."""
    board = trello.Board(
        organization=make_organization(),
        board_id=uuid.uuid1(),
        name=f"board_{board_id}"
    )
    mock_board = mock.MagicMock(return_value=board)
    mock_board.all_lists = [make_list(board, i) for i in range(list_count)]

    return mock_board


def make_list(board, list_id):
    """Creates a list with a new name each time the function is called."""
    return trello.List(
        board=board,
        list_id=uuid.uuid1(),
        name=f"list_{list_id}"
    )


def mock_trello_service(board_count, list_counts=[]):
    """Stubs out the TrelloService for testing purposes."""
    assert(board_count is len(list_counts))

    trello_service = mock.MagicMock()
    trello_service.boards = [make_board(i, list_counts[i]) for i in range(board_count)]

    return trello_service
