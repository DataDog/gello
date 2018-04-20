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

from mock import patch
from app.services import RepoService
from app import db
from app.models import Repo
from tests.base_test_case import BaseTestCase
from tests.utils import mock_github_service


class PatchClass:
    """A class used to patch the `RepoService` constructor."""

    def __init__(self):
        self.github_service = mock_github_service(repo_count=3)


class RepoServiceTestCase(BaseTestCase):
    """Tests the `RepoService` service."""

    @patch('app.services.RepoService.__init__', new=PatchClass.__init__)
    def test_fetch(self):
        """
        Tests the 'fetch' method, and validates it inserts the repos into the
        database.
        """
        repo_service = RepoService()

        repos = Repo.query.all()
        self.assertTrue(len(repos) is 0)

        # Fetch and insert the repos into the database
        repo_service.fetch()

        updated_repos = Repo.query.all()
        self.assertTrue(len(updated_repos) is 3)

    @patch('app.services.RepoService.__init__', new=PatchClass.__init__)
    def test_fetch_with_update(self):
        """
        Tests the 'fetch' method, and validates it inserts the repos into the
        database.
        """
        repo_id = 0
        github_repo_model = Repo(
            name="old_repo_name",
            url='https://github.com/user/old_repo_name',
            github_repo_id=repo_id
        )
        db.session.add(github_repo_model)

        repo_service = RepoService()

        # Validate record has proper attributes
        repo = Repo.query.filter_by(github_repo_id=repo_id).first()
        self.assertTrue(repo.name == 'old_repo_name')
        self.assertTrue(repo.url == 'https://github.com/user/old_repo_name')

        # Fetch and insert the repos into the database
        repo_service.fetch()

        # Validate record attributes have been updated
        updated = Repo.query.filter_by(github_repo_id=repo_id).first()
        self.assertTrue(updated.name == 'repo_0')
        self.assertTrue(updated.url == 'https://github.com/user/repo_0')
