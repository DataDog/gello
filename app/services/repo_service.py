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

from . import GitHubService
from .. import db
from ..models import Repo


class RepoService(object):
    """CRUD persistent storage service.

    A class with the single responsibility of creating/mutating Repo
    data.
    """

    def __init__(self):
        """Initializes a new RepoService object."""
        self.github_service = GitHubService()

    def fetch(self):
        """Add all the repositories to the Database for the organization."""
        for repo in self.github_service.repos():
            repo_model = Repo(
                name=repo.name,
                url=repo.html_url,
                github_repo_id=repo.id
            )
            # Add repository to database
            db.session.add(repo_model)

        # Persist the repositories
        db.session.commit()

    def delete(self, board_id, repo_id):
        """Deletes an old, persisted repo."""
        pass
