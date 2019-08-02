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

"""github_service.py

Service-helpers for interacting with the GitHub API.
"""

from os import environ
from ..api_clients import GitHubAPIClient


class GitHubService(object):
    """A service class for interacting with the GitHub API."""

    def __init__(self):
        """Initializes a new GitHubService object."""
        self.client = GitHubAPIClient().client()

    def repos(self):
        """Returns an array of the organization's public repos.

        Returns:
            list(github.Repo)
        """
        return self._get_organization().get_repos(type='public')

    def members(self):
        """Returns an array of the organization's members.

        Returns:
            list(github.Member)
        """
        return self._get_organization().get_members()

    def create_github_hook(self, url_root, repo_id):
        """Creates a repository webhook for a given repo.

        Args:
            url_root (str): The webhook url for this Gello server.
            repo_id (int): The id of the repository to create the webhook to.

        Returns:
            int: the id of the newly-created webhook (unique per repo)
        """
        config = {'url': url_root, 'content_type': 'json'}
        events = ['issues', 'issue_comment', 'pull_request',
                  'pull_request_review_comment']

        repo = self.client.get_repo(repo_id)
        hook = repo.create_hook(
            name='web',
            config=config,
            events=events,
            active=True
        )
        return hook.id

    def delete_github_hook(self, webhook_id, repo_id):
        """Deletes a repository webhook from a given repo.

        Args:
            webhook_id (int): The id for the webhook to be deleted.
            repo_id (int): The id of the repository to delete the webhook from.

        Returns:
            None
        """
        repo = self.client.get_repo(repo_id)
        webhook = repo.get_hook(webhook_id)
        webhook.delete()

    def organizations(self):
        """Returns a list of GitHub organizations associated with the API Token.

        Returns:
            list(github.Organization)
        """
        return self.client.get_user().get_orgs()

    def _get_organization(self):
        """Returns a representation of the GitHub organization.

        Returns:
            github.Organization: The organization object corresponding to the
                `GITHUB_ORG_LOGIN` environment variable.
        """
        if 'GITHUB_ORG_LOGIN' not in environ:
            print('Must supply the `GITHUB_ORG_LOGIN` variable.')
            return

        orgs = self.organizations()
        return next(
            o for o in orgs if o.login == environ.get('GITHUB_ORG_LOGIN')
        )
