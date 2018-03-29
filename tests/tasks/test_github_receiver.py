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

import unittest
from app import create_app, db
from app.tasks import GitHubReceiver


# Run the celery tasks synchronously, so you don't need to spin up a celery
# worker to perform unit tests
class GitHubReceiverTestCase(unittest.TestCase):
    """Tests the `GitHubReceiver` celery task."""

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_issue_created_for_autocard_subscription(self):
        pass

    def test_pull_request_created_for_autocard_subscription(self):
        pass
