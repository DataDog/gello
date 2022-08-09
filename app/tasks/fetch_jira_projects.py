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

"""fetch_jira_projects.py

Fetches JIRA projects.
"""

from .db_task import DBTask
from ..services.project_service import ProjectService

# TODO: convert this into a nightly cron job and remove it from the UI; it takes
# far too long to execute and shouldn't be something that can just be clicked by
# whoever is logged in
class FetchJIRAProjects(DBTask):
    """A task to fetches JIRA projects."""

    def __init__(self):
        """Initializes a `FetchJIRAProjects` object for the class."""
        pass

    def run(self):
        """Fetches JIRA projects.

        Args:
            None

        Returns:
            None
        """
        try:
            ProjectService().fetch()
            print("Finished fetching JIRA projects")
        except Exception as error:
            print(error)
