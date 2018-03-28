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

"""issue_service.py

Service-helpers for creating and mutating issue data.
"""

from . import CRUDService
from .. import db
from ..models import Issue


class IssueService(CRUDService):
    """CRUD persistent storage service.

    A class with the single responsibility of creating/mutating Issue
    data.
    """

    def create(self, name, url, github_issue_id, repo_id):
        """Creates and persists a new issue record to the database."""
        issue = Issue(
            name=name,
            url=url,
            github_issue_id=github_issue_id,
            repo_id=repo_id
        )
        db.session.add(issue)

        # Persists the issue
        db.session.commit()

    def update(self):
        """Updates a persisted issue."""
        pass

    def delete(self, github_issue_id):
        """Deletes an old, persisted issue."""
        Issue.query.filter_by(github_issue_id=github_issue_id).delete()
        db.session.commit()
