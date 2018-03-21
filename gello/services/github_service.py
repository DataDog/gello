# -*- coding: utf-8 -*-

"""GithubService
"""

from gello.api_clients import GitHubAPIClient


class GitHubService(object):
    """A service with the single responsibility of interacting with the GitHub API."""

    def __init__(self):
        """Initializes a new GitHubService object."""
        self.api_client = GitHubAPIClient()

    def users(self):
        """Returns a dictionary of the organization's users."""
        pass

    def repos(self):
        """Returns a dictionary of the organization's repos."""
        pass

    def organization(self):
        """Returns a string denoting the organization's name."""
        pass

    def create_github_hook(self, repository):
        """Creates a repository webhook."""
        pass
