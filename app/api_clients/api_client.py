# -*- coding: utf-8 -*-

"""api_client.py

Abstract Class representing an API Client.
"""

from gello.utils.decorators import memoized


class APIClient(object):
    """"""

    @memoized
    def client(self):
        """A memoized client method returning an API object created"""
        pass
