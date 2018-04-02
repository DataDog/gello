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

"""subscribed_list_service.py

Service-helpers for creating and mutating subscribed_list data.
"""

from . import CRUDService
from .. import db
from ..models import SubscribedList


class SubscribedListService(CRUDService):
    """CRUD persistent storage service.

    A class with the single responsibility of creating/mutating SubscribedList
    data.
    """

    def create(self, board_id, repo_id, list_id, trello_member_id=None):
        """Creates and persists a subscribed_list record to the database."""
        subscribed_list = SubscribedList(
            subscription_board_id=board_id,
            subscription_repo_id=repo_id,
            list_id=list_id,
            trello_member_id=trello_member_id
        )
        db.session.add(subscribed_list)

        # Persists the subscribed_list
        db.session.commit()

    def update(self):
        """Updates a persisted subscribed_list's autocard value."""
        pass

    def delete(self, board_id, repo_id, list_id):
        """Deletes an old, persisted subscribed_list."""
        SubscribedList.query.filter_by(
            subscription_board_id=board_id,
            subscription_repo_id=repo_id,
            list_id=list_id
        ).delete()

        # Persist the changes
        db.session.commit()
