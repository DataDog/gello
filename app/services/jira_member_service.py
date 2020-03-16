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

"""jira_member_service.py

Service-helpers for creating and mutating jira_member data.
"""

from . import APIService
from . import JIRAService
from .. import db
from ..models import JIRAMember


class JIRAMemberService(APIService):
    """API persistent storage service.

    A class with the single responsibility of creating/mutating JIRA member
    data.
    """

    def __init__(self):
        """Initializes a new JIRAMemberService object."""
        self.jira_service = JIRAService()

    def fetch(self):
        """Add all the jira_members to the database for the organization."""
        fetched_members = self.jira_service.members()
        persisted_members = JIRAMember.query.all()

        self._update_or_delete_records(fetched_members, persisted_members)
        self._create_records(fetched_members, persisted_members)

        # Persist the changes
        db.session.commit()

    def _update_or_delete_records(self, fetched_members, persisted_members):
        """Updates or deletes `JIRAMember` records in the database.

        Args:
            fetched_members (list(jira.Member)): The list of members fetched
                from the JIRA API.
            persisted_members (list(JIRAMember)): The list of persisted
                members fetched from the database.

        Returns:
            None
        """

        fetched_member_ids = set(map(lambda x: x.accountId, fetched_members))
        fetched_emails = set(map(
            lambda x: x.emailAddress if x.emailAddress else False,
            fetched_members))

        for record in persisted_members:
            if record.jira_member_id in fetched_member_ids:
                # Find the JIRA member by unique string `trello_member_id`
                jira_member = list(
                    filter(
                        lambda x: x.accountId == record.jira_member_id,
                        fetched_members
                    )
                )[0]

                # Update the attributes
                record.email = jira_member.emailAddress
                record.name = jira_member.displayName

            elif record.email in fetched_emails:
                # In case `jira_member_id` changed for an existing `email`
                jira_member = list(
                    filter(
                        lambda x: x.emailAddress and x.emailAddress == record.email,
                        fetched_members
                    )
                )[0]

                # Update the attributes
                record.jira_member_id = jira_member.accountId

            else:
                db.session.delete(record)

    def _create_records(self, fetched_members, persisted_members):
        """Inserts `JIRAMember` records into the database.

        Args:
            fetched_members (list(jira.Member)): The list of members fetched
                from the Trello API.
            persisted_members (list(JIRAMember)): The list of persisted
                members fetched from the database.

        Returns:
            None
        """
        persisted_member_ids = set(
            map(lambda x: x.jira_member_id, persisted_members)
        )
        members_to_create = list(
            filter(lambda x: x.accountId not in persisted_member_ids, fetched_members)
        )

        for jira_member in members_to_create:
            jira_member_model = JIRAMember(
                email=jira_member.emailAddress,
                name=jira_member.displayName,
                jira_member_id=jira_member.accountId
            )
            db.session.add(jira_member_model)
