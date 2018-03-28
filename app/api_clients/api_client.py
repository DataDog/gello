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

"""api_client.py

Abstract Class representing an API Client.
"""


class APIClient(object):
    """Abstract Base Class for API interaction."""

    def client(self):
        """A memoized client method returning an API object created"""
        pass
