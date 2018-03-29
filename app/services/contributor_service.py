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

"""contributor_service.py

Service-helpers for creating and mutating contributor data.
"""

from . import APIService
from . import GitHubService
from .. import db
from ..models import Contributor


class ContributorService(APIService):
    """API persistent storage service.

    A class with the single responsibility of creating/mutating Contributor
    data.
    """

    def __init__(self):
        """Initializes a new ContributorService object."""
        self.github_service = GitHubService()

    def fetch(self):
        """Add all the contributors to the database for the organization."""
        for contributor in self.github_service.members():
            self._insert_or_update(contributor)

        # Persist the contributors
        db.session.commit()

    def _insert_or_update(self, contributor):
        """Inserts or updates the records."""
        record = Contributor.query.filter_by(member_id=contributor.id).first()

        if not record:
            contributor_model = Contributor(
                login=contributor.login,
                member_id=contributor.id
            )
            db.session.add(contributor_model)
        else:
            record.login = contributor.login
