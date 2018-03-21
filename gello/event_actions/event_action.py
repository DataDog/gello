# -*- coding: utf-8 -*-

"""Abstract Class representing celery job to be enqueued and run in a task queue.

EventActions follow the command design pattern.
"""

from celery.task import Task

class EventAction(Task):
    """
    """

    def run(self):
        pass
