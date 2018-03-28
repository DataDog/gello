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

"""base_task.py

Abstract base class for tasks.
"""

from celery.task import Task


class GitHubBaseTask(Task):
    """An abstract base class for GitHub-related tasks."""

    def run(self):
        """Implement in concretion."""
        pass

    def get_scope(self):
        """Returns the scope of the payload (i.e., issue, pull_request)."""
        if 'issue' in self.payload:
            return 'issue'
        elif 'pull_request' in self.payload:
            return 'pull_request'
        else:
            print('Unsupported GitHub scope.')

    def set_scope_data(self):
        """Sets GitHub task data related to the scope of the payload."""
        scope = self.get_scope()

        self._id = self.payload[scope]['id']
        self._title = self.payload[scope]['title']
        self._url = self.payload[scope]['html_url']
        self._body = self.payload[scope]['body']
        self._user = self.payload[scope]['user']['login']
        self._user_url = self.payload[scope]['user']['html_url']
