# -*- coding: utf-8 -*-

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
        self.organization = self._get_organization()

    def users(self):
        """Returns a dictionary of the organization's users."""
        pass

    def repos(self):
        """Returns an array of the organization's public repos."""
        return self.organization.get_repos(type='public')

    def members(self):
        """Returns an array of the organization's members."""
        return self.organization.get_members()

    def create_github_hook(self, repository):
        """Creates a repository webhook."""
        pass

    def _get_organization(self):
        orgs = self.client.get_user().get_orgs()
        return next(
            o for o in orgs if o.login == environ.get('GITHUB_ORG_LOGIN')
        )
