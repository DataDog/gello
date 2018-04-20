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

from unittest import TestCase
from app import create_app, db


class BaseTestCase(TestCase):
    """Tests the `GitHubMemberService` service."""

    def setUp(self):
        # Prepare application
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Prepare database
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
