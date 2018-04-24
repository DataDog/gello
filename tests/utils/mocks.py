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

"""general.py

Testing utils for stubbing classes and methods.
"""

import uuid
import mock
from tests.utils import default_board_id


def mock_card(board_id):
    """Creates a mock trello card."""
    card_id = str(uuid.uuid1())
    trello_card = mock.MagicMock(
        id=card_id,
        board_id=board_id,
        url=f"https://trello.com/c/{card_id}",
        return_value=None
    )
    return trello_card


def mock_github_member(github_member_num):
    """Creates a mock github member."""
    member_id = github_member_num
    member_login = f"github_member_{github_member_num}"

    return mock.MagicMock(
        id=member_id,
        login=member_login,
        return_value=None
    )


def mock_trello_member(trello_member_num):
    """Creates a mock trello member."""
    member_id = f"some_uuid_{trello_member_num}"

    trello_member = mock.MagicMock(
        id=member_id,
        username=f"trello_member_{trello_member_num}",
        return_value=None
    )
    trello_member.full_name = f"Trello Name_{trello_member_num}"

    return trello_member


def mock_repo(repo_num):
    """Creates a mock repo."""
    repo_id = repo_num
    repo_name = f"repo_{repo_num}"

    repo = mock.MagicMock(
        id=repo_id,
        html_url=f"https://github.com/user/{repo_name}",
        return_value=None
    )
    repo.name = repo_name

    return repo


def mock_board(board_num, list_count):
    """Creates a mock board."""
    board_id = str(uuid.uuid1())
    board = mock.MagicMock(
        id=board_id,
        url=f"https://trello.com/b/{board_id}",
        return_value=None
    )
    board.name = f"board_{board_num}",
    board.all_lists.return_value = [
        mock_list(board_id, i) for i in range(list_count)
    ]

    return board


def mock_list(board_id, list_num):
    """Creates a mock list."""
    trello_list = mock.MagicMock(
        board_id=board_id,
        id=str(uuid.uuid1()),
        return_value=None
    )
    trello_list.name = f"list_{list_num}",

    return trello_list


def mock_trello_service(board_count=0, list_counts=[], member_count=0):
    """Stubs out the TrelloService for testing purposes."""
    assert(board_count is len(list_counts))

    trello_service = mock.MagicMock()
    trello_service.boards.return_value = [
        mock_board(i, list_counts[i]) for i in range(board_count)
    ]
    trello_service.members.return_value = [
        mock_trello_member(i) for i in range(member_count)
    ]
    trello_service.create_card.return_value = mock_card(default_board_id)

    return trello_service


def mock_github_service(repo_count=0, member_count=0):
    """Stubs out the GitHubService for testing purposes."""
    github_service = mock.MagicMock()
    github_service.repos.return_value = [
        mock_repo(i) for i in range(repo_count)
    ]
    github_service.members.return_value = [
        mock_github_member(i) for i in range(member_count)
    ]

    return github_service
