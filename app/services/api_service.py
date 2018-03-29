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

"""api_service.py

Service-helpers for creating and mutating data.
"""


class APIService(object):
    """API persistent storage service.

    An abstract class for fetching data from an API, and inserting it into the
    database.
    """

    def fetch(self):
        """Fetches data from an API and inserts in into the database."""
        pass
