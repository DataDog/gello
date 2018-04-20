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
from app.services import GitHubMemberService
from app.models import GitHubMember
from tests.base_test_case import BaseTestCase
from tests.utils import mock_github_service


class PatchClass:
    """A class used to patch the `GitHubMemberService` constructor."""

    def __init__(self):
        self.github_service = mock_github_service(member_count=3)


class GitHubMemberServiceTestCase(BaseTestCase):
    """Tests the `GitHubMemberService` service."""

    @patch('app.services.GitHubMemberService.__init__', new=PatchClass.__init__)
    def test_fetch(self):
        """
        Tests the 'fetch' method, and validates it inserts the github_members
        into the database.
        """
        github_member_service = GitHubMemberService()

        github_members = GitHubMember.query.all()
        self.assertTrue(len(github_members) is 0)

        # Fetch and insert the github_members into the database
        github_member_service.fetch()

        updated_github_members = GitHubMember.query.all()
        self.assertTrue(len(updated_github_members) is 3)

    @patch('app.services.GitHubMemberService.__init__', new=PatchClass.__init__)
    def test_fetch_with_update(self):
        """
        Tests the 'fetch' method, and validates it updates the github_members
        correctly.
        """
        github_member_id = 0
        github_member_model = GitHubMember(
            login='old_github_member_login',
            member_id=github_member_id
        )
        db.session.add(github_member_model)

        github_member_service = GitHubMemberService()

        # Validate record has proper attributes
        github_member = GitHubMember.query.filter_by(
            member_id=github_member_id
        ).first()
        self.assertTrue(github_member.login == 'old_github_member_login')

        # Fetch and insert the github_members into the database
        github_member_service.fetch()

        # Validate record attributes have been updated
        updated = GitHubMember.query.filter_by(
            member_id=github_member_id
        ).first()
        self.assertTrue(updated.login == 'github_member_0')
