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

from .api_service import APIService
from .github_service import GitHubService
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
        """Add all the github_members to the database for the organization.

        Returns:
            None
        """
        fetched_members = self.github_service.members()
        persisted_members = GitHubMember.query.all()

        self._update_or_delete_records(fetched_members, persisted_members)
        self._create_records(fetched_members, persisted_members)

        # Persist the changes
        db.session.commit()

    def _get_member_ids(self, fetched_members):
        page_index = 0
        fetched_member_ids = []
        while True:
            current_page = fetched_members.get_page(page_index)
            self.github_service.rate_limit_sleep()

            if not current_page:
                break
            fetched_member_ids += [repo.id for repo in current_page]
            page_index += 1

        return fetched_member_ids

    def _update_or_delete_records(self, fetched_members, persisted_members):
        """Updates or deletes `GitHubMember` records in the database.

        Args:
            fetched_members (list(github.Member)): The list of members fetched
                from the GitHub API.
            persisted_members (list(GitHubMember)): The list of persisted
                members fetched from the database.

        Returns:
            None
        """
        fetched_member_ids = self._get_member_ids(fetched_members)

        for record in persisted_members:
            if record.member_id in fetched_member_ids:
                # Find the github member by unique string `member_id`
                github_member = list(
                    filter(lambda x: x.id == record.member_id, fetched_members)
                )[0]

                # Update the attributes
                record.login = github_member.login
            else:
                db.session.delete(record)

    def _create_records(self, fetched_members, persisted_members):
        """Inserts `GitHubMember` records into the database.

        Args:
            fetched_members (list(github.Member)): The list of members fetched
                from the GitHub API.
            persisted_members (list(GitHubMember)): The list of persisted
                members fetched from the database.

        Returns:
            None
        """
        persisted_member_ids = list(
            map(lambda x: x.member_id, persisted_members)
        )
        members_to_create = list(
            filter(lambda x: x.id not in persisted_member_ids, fetched_members)
        )

        for github_member in members_to_create:
            github_member_model = GitHubMember(
                login=github_member.login,
                member_id=github_member.id
            )
            db.session.add(github_member_model)
