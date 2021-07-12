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

Task-specific initialization code.
"""

from .. import celery

from .github_base_task import GitHubBaseTask
from .delete_trello_card import DeleteCardObjectFromDatabase
from .delete_jira_issue import DeleteJIRAIssueObjectFromDatabase
from .create_github_webhook import CreateGitHubWebhook
from .delete_github_webhook import DeleteGitHubWebhook
from .upsert_github_org_webhook import UpsertGitHubOrgWebhook
from .create_jira_issue import CreateJIRAIssue
from .create_issue_issue import CreateIssueIssue
from .create_pull_request_issue import CreatePullRequestIssue
from .create_trello_card import CreateTrelloCard
from .create_issue_card import CreateIssueCard
from .create_pull_request_card import CreatePullRequestCard
from .create_manual_card import CreateManualCard
from .create_manual_issue import CreateManualIssue
from .update_issue_card_labels import UpdateIssueCardLabels
from .update_jira_issue_labels import UpdateJiraIssueLabels
from .update_pull_request_card_labels import UpdatePullRequestCardLabels
from .update_jira_pull_request_issue_labels import UpdateJiraPullRequestIssueLabels
from .append_jira_issue_labels import AppendJiraIssueLabels
from .append_jira_pull_request_issue_labels import AppendJiraPullRequestIssueLabels
from .github_receiver import GitHubReceiver
from .fetch_jira_projects import FetchJIRAProjects

def _register_tasks():
    """Registers class based celery tasks with celery worker."""
    celery.tasks.register(GitHubBaseTask())
    celery.tasks.register(DeleteCardObjectFromDatabase())
    celery.tasks.register(DeleteJIRAIssueObjectFromDatabase())
    celery.tasks.register(CreateJIRAIssue())
    celery.tasks.register(CreateIssueIssue())
    celery.tasks.register(CreatePullRequestIssue())
    celery.tasks.register(CreateTrelloCard())
    celery.tasks.register(CreateIssueCard())
    celery.tasks.register(CreateManualCard())
    celery.tasks.register(CreateManualIssue())
    celery.tasks.register(CreatePullRequestCard())
    celery.tasks.register(CreateGitHubWebhook())
    celery.tasks.register(DeleteGitHubWebhook())
    celery.tasks.register(UpsertGitHubOrgWebhook())
    celery.tasks.register(UpdateIssueCardLabels())
    celery.tasks.register(UpdateJiraIssueLabels())
    celery.tasks.register(UpdatePullRequestCardLabels())
    celery.tasks.register(UpdateJiraPullRequestIssueLabels())
    celery.tasks.register(GitHubReceiver())
    celery.tasks.register(FetchJIRAProjects())
    celery.tasks.register(AppendJiraIssueLabels())
    celery.tasks.register(AppendJiraPullRequestIssueLabels())

_register_tasks()
