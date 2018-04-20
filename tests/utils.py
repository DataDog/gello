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


BASE_MEMBER_NUM = 0
BASE_REPO_NUM = 0


def make_github_member(github_member_num):
    """Creates a mock repo."""
    member_id = BASE_MEMBER_NUM + github_member_num
    member_login = f"github_member_{github_member_num}"

    return mock.MagicMock(
        id=member_id,
        login=member_login,
        return_value=None
    )


def make_repo(repo_num):
    """Creates a mock repo."""
    repo_id = BASE_REPO_NUM + repo_num
    repo_name = f"repo_{repo_num}"

    repo = mock.MagicMock(
        id=repo_id,
        html_url=f"https://github.com/user/{repo_name}",
        return_value=None
    )
    repo.name = repo_name

    return repo


def make_board(board_num, list_count):
    """Creates a mock board."""
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
    """Creates a mock list."""
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


def mock_github_service(repo_count=0, member_count=0):
    """Stubs out the GitHubService for testing purposes."""
    github_service = mock.MagicMock()
    github_service.repos.return_value = [
        make_repo(i) for i in range(repo_count)
    ]
    github_service.members.return_value = [
        make_github_member(i) for i in range(member_count)
    ]

    return github_service
