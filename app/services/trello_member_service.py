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

"""trello_member_service.py

Service-helpers for creating and mutating trello_member data.
"""

from . import APIService
from . import TrelloService
from .. import db
from ..models import TrelloMember


class TrelloMemberService(APIService):
    """API persistent storage service.

    A class with the single responsibility of creating/mutating Trello member
    data.
    """

    def __init__(self):
        """Initializes a new TrelloMemberService object."""
        self.trello_service = TrelloService()

    def fetch(self):
        """Add all the trello_members to the database for the organization."""
        fetched_members = self.trello_service.members()
        persisted_members = TrelloMember.query.all()

        self._update_or_delete_records(fetched_members, persisted_members)
        self._create_records(fetched_members, persisted_members)

        # Persist the changes
        db.session.commit()

    def _update_or_delete_records(self, fetched_members, persisted_members):
        """Updates or deletes `TrelloMember` records in the database.

        Args:
            fetched_members (list(trello.Member)): The list of members fetched
                from the Trello API.
            persisted_members (list(TrelloMember)): The list of persisted
                members fetched from the database.

        Returns:
            None
        """
        fetched_member_ids = list(map(lambda x: x.id, fetched_members))
        fetched_usernames = list(map(lambda x: x.username, fetched_members))

        for record in persisted_members:
            if record.trello_member_id in fetched_member_ids:
                # Find the trello member by unique string `trello_member_id`
                trello_member = list(
                    filter(
                        lambda x: x.id == record.trello_member_id,
                        fetched_members
                    )
                )[0]

                # Update the attributes
                record.name = trello_member.full_name
                record.username = trello_member.username

            elif record.username in fetched_usernames:
                # In case `trello_member_id` changed for an existing `username`
                trello_member = list(
                    filter(
                        lambda x: x.username == record.username,
                        fetched_members
                    )
                )[0]

                # Update the attributes
                record.name = trello_member.full_name
                record.trello_member_id = trello_member.id

            else:
                db.session.delete(record)

    def _create_records(self, fetched_members, persisted_members):
        """Inserts `TrelloMember` records into the database.

        Args:
            fetched_members (list(trello.Member)): The list of members fetched
                from the Trello API.
            persisted_members (list(TrelloMember)): The list of persisted
                members fetched from the database.

        Returns:
            None
        """
        persisted_member_ids = list(
            map(lambda x: x.trello_member_id, persisted_members)
        )
        members_to_create = list(
            filter(lambda x: x.id not in persisted_member_ids, fetched_members)
        )

        for trello_member in members_to_create:
            trello_member_model = TrelloMember(
                name=trello_member.full_name,
                username=trello_member.username,
                trello_member_id=trello_member.id
            )
            db.session.add(trello_member_model)
