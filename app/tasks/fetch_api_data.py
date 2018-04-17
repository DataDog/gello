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

Fetches API data asynchronously.
"""

from celery.task import Task
from ..services import api_services


class FetchAPIData(Task):
    """A class that fetches API data from `APIService`s."""

    def run(self):
        """Fetches data asynchronously from GitHub and Trello.

        Returns:
            None
        """
        print("Fetching API data asynchronously.")

        # Fetch the API Service data on deployment
        for api_service in api_services():
            api_service.fetch()

        print("Finished fetching API data.")
