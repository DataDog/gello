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

"""subscription_service.py

Service-helpers for creating and mutating subscription data.
"""

from . import CRUDService, SubscribedListService
from .. import db
from ..models import Subscription


class SubscriptionService(CRUDService):
    """CRUD persistent storage service.

    A class with the single responsibility of creating/mutating Subscription
    data.
    """

    def __init__(self):
        self._subscribed_list_service = SubscribedListService()

    def create(self, board_id, repo_id, issue_autocard, pull_request_autocard,
               list_ids=[]):
        """Creates and persists a new subscription record to the database."""
        subscription = Subscription(
            board_id=board_id,
            repo_id=repo_id,
            issue_autocard=issue_autocard,
            pull_request_autocard=pull_request_autocard
        )
        db.session.add(subscription)

        # Create all the subscribed lists
        for list_id in list_ids:
            self._subscribed_list_service.create(
                board_id=board_id,
                repo_id=repo_id,
                list_id=list_id
            )

        # Persists the subscription
        db.session.commit()

    def update(self, board_id, repo_id, issue_autocard, pull_request_autocard):
        """Updates a persisted subscription's autocard value."""
        subscription = Subscription.query.get([board_id, repo_id])
        if issue_autocard is not None:
            subscription.issue_autocard = issue_autocard
        if pull_request_autocard is not None:
            subscription.pull_request_autocard = pull_request_autocard

        # Persist the changes
        db.session.commit()

    def delete(self, board_id, repo_id):
        """Deletes an old, persisted subscription."""
        subscription = Subscription.query.filter_by(
            board_id=board_id, repo_id=repo_id).first()

        # Delete the record
        db.session.delete(subscription)
