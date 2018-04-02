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
        for trello_member in self.trello_service.members():
            self._insert_or_update(trello_member)

        # Persist the trello_members
        db.session.commit()

    def _insert_or_update(self, trello_member):
        """Inserts or updates the records."""
        record = TrelloMember.query.filter_by(
            trello_member_id=trello_member.id).first()

        if not record:
            trello_member_model = TrelloMember(
                name=trello_member.full_name,
                trello_member_id=trello_member.id
            )
            db.session.add(trello_member_model)
        else:
            record.name = trello_member.full_name
