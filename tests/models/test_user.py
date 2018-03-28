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
from app.models import User


class UserTestCase(unittest.TestCase):
    """Tests the `User` model."""

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter_creates_password_hash(self):
        user = User(password='some_random_password')
        self.assertTrue(user.password_hash is not None)

    def test_password_getter_raises_attribute_error(self):
        user = User(password='some_random_password')
        with self.assertRaises(AttributeError):
            user.password
