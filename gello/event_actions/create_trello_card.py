# -*- coding: utf-8 -*-

"""Abstract Class representing celery job to be run
"""

from gello.event_actions.event_action import EventAction


class CreateTrelloCard(EventAction):
    """A task to create a Trello card with a given name and url"""

    def run(self, name, url):
        # TODO: use logger instead
        print(f"Create trello card with {name} and {url}")
