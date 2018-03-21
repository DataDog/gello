# -*- coding: utf-8 -*-

"""Abstract Base Class for
"""

from celery.task import Task


class EventReceiver(Task):
    """A class that receives webhooks from some external API."""

    def run(self):
        """"""
        pass
