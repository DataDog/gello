# -*- coding: utf-8 -*-

"""Concrete class representing
"""

from os import environ
from github import Github
from gello.api_clients import APIClient
from gello.utils.decorators import memoized


class GitHubAPIClient(APIClient):
    """
    A class with the single responsibility of configuring and providing an API
    client to interact with the GitHub API.
    """

    @memoized
    def client(self):
        """
        @return
        """
        return Github(environ.get('GITHUB_API_TOKEN'))
