# -*- coding: utf-8 -*-

"""subscription_service.py

Service-helpers for creating and mutating subscription data.
"""

from .. import db
from ..models import Subscription


class SubscriptionService(object):
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

    def delete(self, board_id, repo_id):
        """Deletes an old, persisted subscription."""
        pass
