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

"""repo_service.py

Service-helpers for creating and mutating repo data.
"""

from . import APIService
from . import GitHubService
from .. import db
from ..models import Repo


class RepoService(APIService):
    """API persistent storage service.

    A class with the single responsibility of creating/mutating Repo
    data.
    """

    def __init__(self):
        """Initializes a new RepoService object."""
        self.github_service = GitHubService()

    def fetch(self):
        """Add all the repositories to the Database for the organization."""
        for repo in self.github_service.repos():
            self._insert_or_update(repo)

        # Persist the repositories
        db.session.commit()

    def _insert_or_update(self, repo):
        """Inserts or updates the records.

        Args:
            repo (github.Repo): The repository to be inserted into the database
                if it doesn't exist, or updated if it does.

        Returns:
            None
        """
        record = Repo.query.filter_by(github_repo_id=repo.id).first()

        if not record:
            repo_model = Repo(
                name=repo.name,
                url=repo.html_url,
                github_repo_id=repo.id
            )
            # Add repository to database
            db.session.add(repo_model)
        else:
            record.name = repo.name
            record.url = repo.html_url
