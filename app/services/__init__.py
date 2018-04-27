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

"""__init__.py

Service helper classes.
"""

from .api_service import APIService
from .crud_service import CRUDService
from .github_service import GitHubService
from .trello_service import TrelloService
from .board_service import BoardService
from .subscribed_list_service import SubscribedListService
from .subscription_service import SubscriptionService
from .repo_service import RepoService
from .github_member_service import GitHubMemberService
from .trello_member_service import TrelloMemberService
from .issue_service import IssueService
from .pull_request_service import PullRequestService
from .config_value_service import ConfigValueService
from .environment_variable_service import EnvironmentVariableService


def api_services():
    """Returns a list of services which implement the APIService interface."""
    return [
        GitHubMemberService(),
        TrelloMemberService(),
        RepoService(),
        BoardService()
    ]
