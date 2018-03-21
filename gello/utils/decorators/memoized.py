# -*- coding: utf-8 -*-

"""Memoized

A decorator to provide memoization functionality, similar to Ruby's.
"""

import collections
import functools


class memoized(object):
    """Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    """
    def __init__(self, func):
        """Initializes a new memoized object."""
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        # uncacheable. a list, for instance.
        # better to not cache than blow up.
        if not isinstance(args, collections.Hashable):
            return self.func(*args)

        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value

    def __repr__(self):
        """Return the function"s docstring."""
        return self.func.__doc__

    def __get__(self, obj, objtype):
        """Support instance methods."""
        return functools.partial(self.__call__, obj)
