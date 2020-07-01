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
import time

from ..api_clients import GitHubAPIClient
from ..models import ConfigValue
from .config_value_service import ConfigValueService


class GitHubService(object):
    """A service class for interacting with the GitHub API."""

    def __init__(self):
        """Initializes a new GitHubService object."""
        self.client = GitHubAPIClient().client()
        self._config_value_service = ConfigValueService()

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

    def rate_limit_sleep(self):
        """Sleep after making a request to Github API.
        Adhering to Github's rate limit of 5000 requests per hour: https://developer.github.com/v3/#rate-limiting
        Delay calculation: 5000 requests / 3600 seconds (in an hour) = 1.39.
        Rounded up to 1.5 for buffer. Specifically, 5000*1.5-5000*1.39 = 550 more requests.

        Returns:
            None
        """
        time.sleep(1.5)

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

    def create_github_org_hook(self, url_root):
        """Creates a repository webhook for a given repo.

        Args:
            url_root (str): The webhook url for this Gello server.

        Returns:
            int: the id of the newly-created webhook (unique per org)
        """
        config = {'url': url_root, 'content_type': 'json'}
        events = ['organization']

        org = self._get_organization()
        hook = org.create_hook(
            name='web',
            config=config,
            events=events,
            active=True
        )
        return hook.id

    def get_org_webhook(self, url_root):
        """Gets a organization webhook.

        Args:
            url_root (str): The webhook url for this Gello server.

        Returns:
            github.Hook.Hook: The Github organization webhook object with `url_root` as the url.
        """
        # TODO(URSULA): Clean this up once Github Pagination API totalCount does not throw an exception
        # (https://pygithub.readthedocs.io/en/latest/utilities.html#github.PaginatedList.PaginatedList)
        try:
            total_count = self._get_organization().get_hooks().totalCount
        except UnknownObjectException as e:
            print("github.GithubException.UnknownObjectException:", e)
            total_count = 0
        
        hooks = self._get_organization().get_hooks() if total_count > 0 else []

        for hook in hooks:
            if (hook.config['url'] == url_root or
                    (hook.config['url'][-1] != '/' and hook.config['url'] + "/" == url_root)):
                return hook
        return None

    def update_webhook_events(self, existing_hook, list_of_events):
        """Updates the organization webhook with a list of events.

        Args:
            existing_hook (github.Hook.Hook): The Github organization webhook object.
            list_of_events (List[str]): A list of events to be added to the webhook triggers.

        Returns:
            None
        """
        hook = self._get_organization().get_hook(existing_hook.id)
        hook.edit(
            name='web',
            config=existing_hook.config,
            events=existing_hook.events + list_of_events,
            active=True
        )

    def upsert_webhook(self, webhook_id):
        """Adds or updates `GITHUB_ORG_WEBHOOK_ID` as a Config Value.

        Args:
            webhook_id (int): The GitHub-issued id for org webhook.

        Returns:
            None
        """
        self._config_value_service.create(key='GITHUB_ORG_WEBHOOK_ID', value=str(webhook_id))

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
                `GITHUB_ORG_LOGIN` config value.
        """
        if not ConfigValue.query.get('GITHUB_ORG_LOGIN'):
            print('Must supply the `GITHUB_ORG_LOGIN` config value.')
            return

        orgs = self.organizations()
        return next(
            o for o in orgs if o.login == ConfigValue.query.get('GITHUB_ORG_LOGIN').value
        )
