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

"""database.py

Testing utils for creating database records needed for associations.
"""

from tests.utils import default_board_id, default_repo_id, default_list_id
from app import db
from app.models import Board, List, Repo, Subscription, SubscribedList


def create_board():
    """Create the board needed for the foreign key constraint."""
    db.session.add(
        Board(
            name='board_name',
            url=f"https://trello.com/b/{default_board_id}",
            trello_board_id=default_board_id
        )
    )


def create_repo():
    """Create the repo needed for the foreign key constraint."""
    db.session.add(
        Repo(
            name='repo_name',
            url='https://github.com/user/repo',
            github_repo_id=default_repo_id
        )
    )


def create_list():
    """Create the list needed for the foreign key constraint."""
    db.session.add(
        List(
            name='list_name',
            trello_list_id=default_list_id,
            board_id=default_board_id
        )
    )


def create_subscription():
    """Create a subscription."""
    db.session.add(
        Subscription(
            board_id=default_board_id,
            repo_id=default_repo_id,
            issue_autocard=True,
            pull_request_autocard=True
        )
    )


def create_subscribed_list():
    """Create a subscribed list to create cards for."""
    db.session.add(
        SubscribedList(
            subscription_board_id=default_board_id,
            subscription_repo_id=default_repo_id,
            list_id=default_list_id
        )
    )
