# -*- coding: utf-8 -*-

"""github_api_client.py

Concrete class representing GitHub API Client.
"""

from os import environ
from github import Github
from . import APIClient


class GitHubAPIClient(APIClient):
    """
    A class with the single responsibility of configuring and providing an API
    client to interact with the GitHub API.
    """

    def __init__(self):
        self._client = Github(environ.get('GITHUB_API_TOKEN'))

    def client(self):
        return self._client
