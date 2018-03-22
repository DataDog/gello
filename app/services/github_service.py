# -*- coding: utf-8 -*-

"""github_service.py

Service-helpers for interacting with the GitHub API.
"""

from ..api_clients import GitHubAPIClient


class GitHubService(object):
    """A service class for interacting with the GitHub API."""

    def __init__(self):
        """Initializes a new GitHubService object."""
        self.client = GitHubAPIClient().client()

    def users(self):
        """Returns a dictionary of the organization's users."""
        pass

    def repos(self):
        """Returns a dictionary of the organization's repos."""
        return self.client.get_user().get_repos()

    def organization(self):
        """Returns a string denoting the organization's name."""
        pass

    def create_github_hook(self, repository):
        """Creates a repository webhook."""
        pass
