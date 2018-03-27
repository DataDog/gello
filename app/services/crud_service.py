# -*- coding: utf-8 -*-

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
