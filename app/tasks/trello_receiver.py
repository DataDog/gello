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

"""trello_receiver.py

Concrete Class representing receiver from Trello webhooks. Each receiver is a
celery task, which is enqueued in the receivers task queue.
"""

from celery.task import Task
from ..models import Board, Subscription, TrelloMember


class TrelloReceiver(Task):
    """A class that receives webhooks from some the Trello API."""

    def run(self, payload):
        """Handles Trello webhook events.

        Args:
            payload (dict): The JSON response from the Trello webhook -
                deserialized as a Python `dict`.

        Returns:
            None
        """
        print('Run Trello receiver task.')
        self.payload = payload
