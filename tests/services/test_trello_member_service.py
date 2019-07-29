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

from mock import patch
from app import db
from app.services import TrelloMemberService
from app.models import TrelloMember
from tests.base_test_case import BaseTestCase
from tests.utils import mock_trello_service


class PatchClass:
    """A class used to patch the `TrelloMemberService` constructor."""

    def __init__(self):
        self.trello_service = mock_trello_service(member_count=3)


class TrelloMemberServiceTestCase(BaseTestCase):
    """Tests the `TrelloMemberService` service."""

    @patch('app.services.TrelloMemberService.__init__', new=PatchClass.__init__)
    def test_fetch(self):
        """
        Tests the 'fetch' method, and validates it inserts the trello_members
        into the database.
        """
        trello_member_service = TrelloMemberService()

        trello_members = TrelloMember.query.all()
        self.assertTrue(len(trello_members) is 0)

        # Fetch and insert the trello_members into the database
        trello_member_service.fetch()

        updated_trello_members = TrelloMember.query.all()
        self.assertTrue(len(updated_trello_members) is 3)

    @patch('app.services.TrelloMemberService.__init__', new=PatchClass.__init__)
    def test_fetch_with_updated_username(self):
        """
        Tests the 'fetch' method, and validates it updates Trello username
        correctly.
        """
        trello_member_id = "some_uuid_0"
        trello_member_model = TrelloMember(
            name='Old Name',
            username='old_trello_member_username',
            trello_member_id=trello_member_id
        )
        db.session.add(trello_member_model)

        trello_member_service = TrelloMemberService()

        # Validate record has proper attributes
        trello_member = TrelloMember.query.filter_by(
            trello_member_id=trello_member_id
        ).first()
        self.assertTrue(trello_member.name == 'Old Name')
        self.assertTrue(trello_member.username == 'old_trello_member_username')

        # Fetch and insert the trello_members into the database
        trello_member_service.fetch()

        # Validate record attributes have been updated
        updated = TrelloMember.query.filter_by(
            trello_member_id=trello_member_id
        ).first()
        self.assertTrue(updated.name == 'Trello Name_0')
        self.assertTrue(updated.username == 'trello_member_0')

    # FIXME: change update username to update memberid
    @patch('app.services.TrelloMemberService.__init__', new=PatchClass.__init__)
    def test_fetch_with_updated_member_id(self):
        """
        Tests the 'fetch' method, and validates it updates Trello member ID
        correctly.
        """
        trello_username = 'trello_member_0'
        trello_member_model = TrelloMember(
            name='Old Name',
            username=trello_username,
            trello_member_id='some_uuid_old'
        )
        db.session.add(trello_member_model)

        trello_member_service = TrelloMemberService()

        # Validate record has proper attributes
        trello_member = TrelloMember.query.filter_by(
            username=trello_username
        ).first()
        self.assertTrue(trello_member.name == 'Old Name')
        self.assertTrue(trello_member.trello_member_id == 'some_uuid_old')

        # Fetch and insert the trello_members into the database
        trello_member_service.fetch()

        # Validate record attributes have been updated
        updated = TrelloMember.query.filter_by(
            username=trello_username
        ).first()
        self.assertTrue(updated.name == 'Trello Name_0')
        self.assertTrue(updated.trello_member_id == 'some_uuid_0')
