# -*- coding: utf-8 -*-

"""subscription_service.py

Service-helpers for creating and mutating subscription data.
"""

from . import CRUDService
from .. import db
from ..models import Subscription


class SubscriptionService(CRUDService):
    """CRUD persistent storage service.

    A class with the single responsibility of creating/mutating Subscription
    data.
    """

    def create(self, board_id, repo_id, autocard):
        """Creates and persists a new subscription record to the database."""
        subscription = Subscription(
            board_id=board_id,
            repo_id=repo_id,
            autocard=autocard
        )
        db.session.add(subscription)

        # Persists the subscription
        db.session.commit()

    def update(self, board_id, repo_id, autocard):
        """Updates a persisted subscription's autocard value."""
        subscription = Subscription.query.get([board_id, repo_id])
        subscription.autocard = autocard

        # Persist the changes
        db.session.commit()

    def delete(self, board_id, repo_id):
        """Deletes an old, persisted subscription."""
        Subscription.query.filter_by(
            board_id=board_id, repo_id=repo_id).delete()

        # Persist the changes
        db.session.commit()
