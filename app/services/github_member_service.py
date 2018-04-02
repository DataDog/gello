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

"""github_member_service.py

Service-helpers for creating and mutating github_member data.
"""

from . import APIService
from . import GitHubService
from .. import db
from ..models import GitHubMember


class GitHubMemberService(APIService):
    """API persistent storage service.

    A class with the single responsibility of creating/mutating GitHub member
    data.
    """

    def __init__(self):
        """Initializes a new GitHubMemberService object."""
        self.github_service = GitHubService()

    def fetch(self):
        """Add all the github_members to the database for the organization."""
        for github_member in self.github_service.members():
            self._insert_or_update(github_member)

        # Persist the github_members
        db.session.commit()

    def _insert_or_update(self, github_member):
        """Inserts or updates the records."""
        record = GitHubMember.query.filter_by(
            member_id=github_member.id).first()

        if not record:
            github_member_model = GitHubMember(
                login=github_member.login,
                member_id=github_member.id
            )
            db.session.add(github_member_model)
        else:
            record.login = github_member.login
