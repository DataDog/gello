# -*- coding: utf-8 -*-

"""contributor_service.py

Service-helpers for creating and mutating contributor data.
"""

from . import GitHubService
from .. import db
from ..models import Contributor


class ContributorService(object):
    """CRUD persistent storage service.

    A class with the single responsibility of creating/mutating Contributor
    data.
    """

    def __init__(self):
        """Initializes a new ContributorService object."""
        self.github_service = GitHubService()

    def fetch(self):
        """Add all the contributors to the Database for the organization."""
        for contributor in self.github_service.members():
            contributor_model = Contributor(
                login=contributor.login,
                member_id=contributor.id
            )
            db.session.add(contributor_model)

        # persist the contributors
        db.session.commit()

    def delete(self, board_id, contributor_id):
        """Deletes an old, persisted contributor."""
        pass
