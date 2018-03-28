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

"""pull_request_service.py

Service-helpers for creating and mutating pull_request data.
"""

from . import CRUDService
from .. import db
from ..models import PullRequest


class PullRequestService(CRUDService):
    """CRUD persistent storage service.

    A class with the single responsibility of creating/mutating PullRequest
    data.
    """

    def create(self, name, url, github_pull_request_id, repo_id):
        """Creates and persists a new pull_request record to the database."""
        pull_request = PullRequest(
            name=name,
            url=url,
            github_pull_request_id=github_pull_request_id,
            repo_id=repo_id
        )
        db.session.add(pull_request)

        # Persists the pull_request
        db.session.commit()

    def update(self):
        """Updates a persisted pull_request."""
        pass

    def delete(self, github_pull_request_id):
        """Deletes an old, persisted pull_request."""
        PullRequest.query.filter_by(
               github_pull_request_id=github_pull_request_id).delete()
        db.session.commit()
