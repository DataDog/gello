# -*- coding: utf-8 -*-

"""Abstract Class representing
"""

from gello.utils.decorators import memoized


class APIClient(object):
    """"""

    @memoized
    def client(self):
        """A memoized client method returning an API object created
        """
        pass
