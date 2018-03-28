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

"""CRUD_service.py

Service-helpers for creating and data.
"""


class CRUDService(object):
    """CRUD persistent storage service.

    An abstract class for creating and mutating data.
    """

    def create(self):
        """Creates and persists a new record to the database."""
        pass

    def update(self):
        """Updates a persisted record."""
        pass

    def delete(self):
        """Deletes a persisted record."""
        pass
