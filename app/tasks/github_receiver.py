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

"""github_receiver.py

Concrete Class representing receiver from GitHub webhooks. Each receiver is a
celery task, which is enqueued in the receivers task queue.
"""

from . import CreateIssueCard
from . import CreateIssueIssue
from . import CreateManualCard
from . import CreateManualIssue
from . import CreatePullRequestCard
from . import CreatePullRequestIssue
from . import DeleteCardObjectFromDatabase
from . import DeleteJIRAIssueObjectFromDatabase
from . import GitHubBaseTask
from . import UpdateIssueCardLabels
from . import UpdateJiraIssueLabels
from . import UpdateJiraPullRequestIssueLabels
from . import UpdatePullRequestCardLabels
from . import AppendJiraIssueLabels
from . import AppendJiraPullRequestIssueLabels
from ..models import ConfigValue
from ..models import GitHubMember
from ..models import Issue
from ..models import PullRequest
from ..models import Repo
from ..models import Subscription
from config import Config
from ..services import GitHubMemberService
from ..services import TrelloService


class GitHubReceiver(GitHubBaseTask):
    """A class that receives webhooks from some the GitHub API."""

    def run(self, payload):
        """Performs validations on the event type and enqueues them.

        Validates the event being received is a GitHub Pull Request event or a
        GitHub Issue event, and then enqueues it in the corresponding events
        queue.

        Args:
            payload (dict): The card-specific data, used in the `_card_body`
                            template method.

        Returns:
            None
        """
        print('Run GitHub receiver task.')
        self.payload = payload
        self._enqueue_tasks()

    def _enqueue_tasks(self):
        """Enqueues tasks based on the payload parameters.

        Enqueues tasks for each of the subscriptions which belong to the
        repository associated by the `github_repo_id`.

        Returns:
            None
        """
        # Ignore all hook payloads
        if "hook" in self.payload:
            return

        # Auto-refresh Github members
        if ((self.payload['action'] == 'member_added' or self.payload['action'] == 'member_removed') and
                self.payload['organization']['login'] == ConfigValue.query.get('GITHUB_ORG_LOGIN').value):
            GitHubMemberService().fetch()
            return
        elif self.payload['action'] == 'member_invited':
            return

        repo = Repo.query.filter_by(
            github_repo_id=self.payload['repository']['id']
        ).first()

        # The repository must exist
        if repo is None:
            print('The repository does not exist in the database.')
            return

        # Get all of the subscriptions related to a repository
        subscriptions = Subscription.query.filter_by(
            repo_id=repo.github_repo_id
        )

        try:
            label_names = [Config.REPO_LABELS[repo.name]]
        except KeyError:
            label_names = []

        # Perform an action for each of the subscribed lists belonging to a
        # subscription
        for subscription in subscriptions:
            for trello_list in subscription.subscribed_lists:
                self._handle_card(
                    board_id=subscription.board_id,
                    list_id=trello_list.list_id,
                    issue_autocard=subscription.issue_autocard,
                    pull_request_autocard=subscription.pull_request_autocard,
                    label_names=label_names,
                    assignee_id=trello_list.trello_member_id
                )
            for jira_project in subscription.subscribed_jira_projects:
                self._handle_jira_issue(
                    project_key=jira_project.subscription_project_key,
                    issue_autocard=subscription.issue_autocard,
                    pull_request_autocard=subscription.pull_request_autocard,
                    label_names=label_names,
                    jira_member_id=jira_project.jira_member_id,
                    issue_type=jira_project.issue_type_id
                )

            for jira_issue_sub in subscription.subscribed_jira_issues:
                self._handle_jira_issue(
                    project_key=jira_issue_sub.subscription_project_key,
                    issue_autocard=subscription.issue_autocard,
                    pull_request_autocard=subscription.pull_request_autocard,
                    label_names=label_names,
                    jira_member_id=jira_issue_sub.jira_member_id,
                    parent_issue=jira_issue_sub.jira_issue_key,
                    issue_type=jira_issue_sub.issue_type_name
                )

    def _handle_jira_issue(self, project_key, issue_autocard,
                           pull_request_autocard, label_names, jira_member_id,
                           parent_issue=None, issue_type=None):
        """Determines which JIRA issue task to enqueue based on the payload
        parameters.

        Args:
            project_key (str): The key of the project to raise an issue on.
            issue_autocard (Boolean): If `autocard` is `true` for Issues
                created.
            pull_request_autocard (Boolean): If `autocard` is `true` for Pull
                Requests created.
            label_names (List[str]): A list of label names.
            jira_member_id (str): The user id for the JIRA Issue assignee.
            parent_issue (str): The key of the parent issue for this sub-issue.
            issue_type (str): The id of the issue type of the project.

        Returns:
            None
        """
        scope = self.get_scope()
        action = self.payload['action']

        if scope == 'issue':
            label_names += [label['name'] for label in self.payload['issue']['labels']]

            if not issue_autocard and 'comment' in self.payload and action == 'created' and \
                    self._manual_command_string() in self.payload['comment']['body']:
                self._create_manual_issue(project_key, label_names, jira_member_id,
                                        parent_issue, issue_type)
            elif not issue_autocard:
                print('Repo not subscribed to Issues.')
            elif action == 'opened':
                self._create_jira_issue_issue(project_key, label_names,
                                            jira_member_id,
                                            parent_issue, issue_type)
            elif action == "labeled" or action == "unlabeled":
                self._update_issue_jira_issue_labels(self.payload['issue']['id'], project_key, label_names)
            elif action == 'closed':
                issue = Issue.query.filter_by(jira_project_key=project_key, github_issue_id=self.payload['issue']['id']).first()
                jira_issue_key = issue.jira_issue_key
                AppendJiraIssueLabels.delay(
                    jira_issue_key,
                    project_key,
                    ["github_closed"],
                    self.payload,
                )
                self._delete_issue_jira_issue_objects()
            else:
                print('Unsupported event action: {0}'.format(action))

        elif scope == "pull_request":
            label_names += [label['name'] for label in self.payload['pull_request']['labels']]

            if not pull_request_autocard and 'comment' in self.payload and action == 'created' and \
                    self._manual_command_string() in self.payload['comment']['body']:
                self._create_manual_issue(project_key, label_names, jira_member_id,
                                        parent_issue, issue_type)
            elif not pull_request_autocard:
                print('Repo not subscribed to PRs.')
            elif action == 'opened':
                self._create_jira_pull_request_issue(
                    project_key, label_names, jira_member_id, parent_issue,
                    issue_type)
            elif action == "labeled" or action == "unlabeled":
                self._update_pull_request_jira_issue_labels(self.payload['pull_request']['id'], project_key, label_names)
            elif action == 'closed':
                pull_request = PullRequest.query.filter_by(jira_project_key=project_key, github_pull_request_id=self.payload["pull_request"]["id"]).first()
                if hasattr(pull_request, 'jira_issue_key'):
                    jira_issue_key = pull_request.jira_issue_key
                    AppendJiraPullRequestIssueLabels.delay(
                        jira_issue_key,
                        project_key,
                        ["github_closed"],
                        self.payload,
                    )
                    self._delete_pull_request_jira_issue_objects()
            else:
                print('Unsupported event action.')
        else:
            print('Unsupported event action.')

    def _handle_card(self, board_id, list_id, issue_autocard,
                     pull_request_autocard, label_names, assignee_id):
        """Determines which trello card task to enqueue based on the payload
        parameters.

        Args:
            board_id (str): The id of the board the card will be created on.
            list_id (str): The id of the list the card will be created on.
            issue_autocard (Boolean): If `autocard` is `true` for Issues
                created.
            pull_request_autocard (Boolean): If `autocard` is `true` for Pull
                Requests created.
            label_names (List[str]): List of label names.
            assignee_id (str): The trello_member_id for the card assignee.

        Returns:
            None
        """
        scope = self.get_scope()
        action = self.payload['action']

        if scope == 'issue':
            label_names += [label['name'] for label in self.payload['issue']['labels']]

            if not issue_autocard and 'comment' in self.payload and action == 'created' and \
                    self._manual_command_string() in self.payload['comment']['body']:
                self._create_manual_card(board_id, list_id, label_names, assignee_id)
            elif issue_autocard and action == 'opened':
                self._create_trello_issue_card(board_id, list_id, label_names, assignee_id)
            elif action == "labeled" or action == "unlabeled":
                self._update_trello_issue_card_labels(self.payload['issue']['id'], board_id, label_names)
            elif action == 'closed':
                self._delete_issue_trello_card_objects()
            else:
                print('Unsupported event action.')
        elif scope == 'pull_request':
            label_names += [label['name'] for label in self.payload['pull_request']['labels']]

            if not pull_request_autocard and 'comment' in self.payload and action == 'created' and \
                    self._manual_command_string() in self.payload['comment']['body']:
                self._create_manual_card(board_id, list_id, label_names, assignee_id)
            elif pull_request_autocard and action == 'opened':
                self._create_trello_pull_request_card(board_id, list_id, label_names, assignee_id)
            elif action == "labeled" or action == "unlabeled":
                self._update_trello_pull_request_card_labels(self.payload['pull_request']['id'], board_id, label_names)
            elif action == 'closed':
                self._delete_pull_request_trello_card_objects()
            else:
                print('Unsupported event action.')
        else:
            print('Unsupported event action.')

    def _create_manual_issue(
        self, project_key, label_names, jira_member_id, parent_issue, issue_type
    ):
        """Creates a task to create a JIRA Issue.

        NOTE: It does not create a card if the user DOES NOT belong to the
        GitHub organization associated with the `GITHUB_ORG_LOGIN`.

        Args:
            project_key (str): The key of the project to raise an issue on.
            label_names (List[str]): A list of label names.
            jira_member_id (str): The user id for the JIRA Issue assignee.
            parent_issue (str): The key of the parent issue for this sub-issue
            (if a sub-issue is to be created)
            issue_type (str): The id of the issue type of the project.

        Returns:
            None
        """
        if not self._user_in_organization():
            print('The user does not belong to the organization.')
            return

        CreateManualIssue.delay(
            project_key=project_key,
            issue_type=issue_type,
            payload=self.payload,
            parent_issue=parent_issue,
            assignee_id=jira_member_id,
            label_names=label_names
        )

    def _create_manual_card(self, board_id, list_id, label_names, assignee_id):
        """Creates a task to create a trello card.

        NOTE: It does not create a card if the user DOES NOT belong to the
        GitHub organization associated with the `GITHUB_ORG_LOGIN`.

        Args:
            board_id (str): The id of the board the card will be created on.
            list_id (str): The id of the list the card will be created on.
            label_names (List[str]): A list of label names.
            assignee_id (str): The trello_member_id for the card assignee.

        Returns:
            None
        """
        if not self._user_in_organization():
            print('The user does not belong to the organization.')
            return

        CreateManualCard.delay(
            board_id=board_id,
            list_id=list_id,
            name=f"Manual card created by {self.payload['sender']['login']}",
            payload=self.payload,
            label_names=label_names,
            assignee_id=assignee_id
        )

    def _create_jira_issue_issue(
        self, project_key, label_names, jira_member_id, parent_issue, issue_type
    ):
        """Creates a task to create a JIRA issue for the corresponding GitHub issue.

        NOTE: It does not create a JIRA issue if the user belongs to the GitHub
        organization associated with the `GITHUB_ORG_LOGIN`.

        Args:
            project_key (str): The key of the project to raise an issue on.
            label_names (List[str]): A list of label names.
            jira_member_id (str): The user id for the JIRA Issue assignee.
            parent_issue (str): The key of the parent issue for this sub-issue
            (if a sub-issue is to be created)
            issue_type (str): The id of the issue type of the project.

        Returns:
            None
        """

        if self._user_in_organization():
            print('The user belongs to the organization, not creating card.')
            return

        CreateIssueIssue.delay(
            project_key=project_key,
            issue_type=issue_type,
            payload=self.payload,
            parent_issue=parent_issue,
            assignee_id=jira_member_id,
            label_names=label_names
        )

    def _create_jira_pull_request_issue(
        self, project_key, label_names, jira_member_id, parent_issue, issue_type
    ):
        """Creates a task to create a JIRA issue for the corresponding GitHub pull
        request.

        NOTE: It does not create a JIRA issue if the user belongs to the GitHub
        organization associated with the `GITHUB_ORG_LOGIN`.

        Args:
            project_key (str): The key of the project to raise an issue on.
            label_names (List[str]): A list of label names.
            jira_member_id (str): The user id for the JIRA Issue assignee.
            parent_issue (str): The key of the parent issue for this sub-issue
            (if a sub-issue is to be created)
            issue_type (str): The id of the issue type of the project.

        Returns:
            None
        """

        if self._user_in_organization():
            print('The user belongs to the organization, not creating card.')
            return

        CreatePullRequestIssue.delay(
            project_key=project_key,
            issue_type=issue_type,
            payload=self.payload,
            parent_issue=parent_issue,
            assignee_id=jira_member_id,
            label_names=label_names
        )

    def _delete_issue_jira_issue_objects(self):
        """Deletes all JIRA issues associated with an issue.

        Returns:
            None
        """
        scope = self.get_scope()
        github_id = self.payload[scope]['id']
        issues = Issue.query.filter_by(github_issue_id=github_id)

        for issue in issues:
            DeleteJIRAIssueObjectFromDatabase.delay(
                scope=scope,
                github_id=github_id
            )

    def _delete_pull_request_jira_issue_objects(self):
        """Deletes all JIRA issues associated with an pull requests.

        Returns:
            None
        """
        scope = self.get_scope()
        github_id = self.payload[scope]['id']
        pull_requests = PullRequest.query.filter_by(
            github_pull_request_id=github_id)

        for pull_request in pull_requests:
            DeleteJIRAIssueObjectFromDatabase.delay(
                scope=scope,
                github_id=github_id
            )

    def _create_trello_issue_card(self, board_id, list_id, label_names, assignee_id):
        """Creates a task to create a trello card.

        NOTE: It does not create a card if the user belongs to the GitHub
        organization associated with the `GITHUB_ORG_LOGIN`.

        Args:
            board_id (str): The id of the board the card will be created on.
            list_id (str): The id of the list the card will be created on.
            label_names (List[str]): A list of label names.
            assignee_id (str): The trello_member_id for the card assignee.

        Returns:
            None
        """
        if self._user_in_organization():
            print('The user belongs to the organization, not creating card.')
            return

        CreateIssueCard.delay(
            board_id=board_id,
            list_id=list_id,
            name=self.payload['issue']['title'],
            payload=self.payload,
            label_names=label_names,
            assignee_id=assignee_id
        )

    def _create_trello_pull_request_card(self, board_id, list_id, label_names, assignee_id):
        """Creates a task to create a trello card.

        NOTE: It does not create a card if the user belongs to the GitHub
        organization associated with the `GITHUB_ORG_LOGIN`.

        Args:
            board_id (str): The id of the board the card will be created on.
            list_id (str): The id of the list the card will be created on.
            label_names (List[str]): A list of label names.
            assignee_id (str): The trello_member_id for the card assignee.

        Returns:
            None
        """
        if self._user_in_organization():
            print('The user belongs to the organization, not creating card.')
            return

        CreatePullRequestCard.delay(
            board_id=board_id,
            list_id=list_id,
            name=self.payload['pull_request']['title'],
            payload=self.payload,
            label_names=label_names,
            assignee_id=assignee_id
        )

    def _update_trello_issue_card_labels(self, issue_id, board_id, label_names):
        """Creates a task to update trello issue card labels.

        Args:
            issue_id (str): The id of the Github issue.
            board_id (str): The id of the board the card was created on.
            label_names (List[str]): A list of label names.

        Returns:
            None
        """
        UpdateIssueCardLabels.delay(
            issue_id=issue_id,
            board_id=board_id,
            label_names=label_names,
            payload=self.payload
        )

    def _update_trello_pull_request_card_labels(self, pull_request_id, board_id, label_names):
        """Creates a task to update trello pull request card labels.

        Args:
            pull_request_id (str): The id of the Github pull request.
            board_id (str): The id of the board the card was created on.
            label_names (List[str]): A list of label names.

        Returns:
            None
        """
        UpdatePullRequestCardLabels.delay(
            pull_request_id=pull_request_id,
            board_id=board_id,
            label_names=label_names,
            payload=self.payload
        )

    def _update_issue_jira_issue_labels(self, issue_id, project_key, label_names):
        """Creates a task to update jira issue labels.

        Args:
            issue_id (str): The id of the Github issue.
            project_key (str): The key of the project that the jira issue was raised on.
            label_names (List[str]): A list of label names.

        Returns:
            None
        """
        UpdateJiraIssueLabels.delay(
            issue_id=issue_id,
            project_key=project_key,
            label_names=label_names,
            payload=self.payload
        )

    def _update_pull_request_jira_issue_labels(self, pull_request_id, project_key, label_names):
        """Creates a task to update jira pull request issue labels.

        Args:
            pull_request_id (str): The id of the Github pull request.
            project_key (str): The key of the project that the jira issue was raised on.
            label_names (List[str]): A list of label names.

        Returns:
            None
        """
        UpdateJiraPullRequestIssueLabels.delay(
            pull_request_id=pull_request_id,
            project_key=project_key,
            label_names=label_names,
            payload=self.payload
        )

    def _delete_issue_trello_card_objects(self):
        """Deletes all trello cards associated with an issue.

        Returns:
            None
        """
        scope = self.get_scope()
        github_id = self.payload[scope]['id']
        issues = Issue.query.filter_by(github_issue_id=github_id)

        for issue in issues:
            # Don't delete issue from database if there is still JIRA work to do
            if issue.jira_issue_key is None:
                DeleteCardObjectFromDatabase.delay(
                    scope=scope,
                    github_id=None,
                    db_id=issue.id
                )

    def _delete_pull_request_trello_card_objects(self):
        """Deletes all trello cards associated with a pull request.

        Returns:
            None
        """
        scope = self.get_scope()
        github_id = self.payload[scope]['id']
        pull_requests = PullRequest.query.filter_by(
            github_pull_request_id=github_id)

        for pull_request in pull_requests:
            # Don't delete PR from database if there is still JIRA work to do
            if pull_request.jira_issue_key is None:
                DeleteCardObjectFromDatabase.delay(
                    scope=scope,
                    github_id=None,
                    db_id=pull_request.id
                )

    def _user_in_organization(self):
        """Checks if the person is in the organization.

        Returns:
            Boolean: `true` if the user belongs to the organization.
        """
        github_member = GitHubMember.query.filter_by(
            member_id=self.payload['sender']['id']
        ).first()

        return github_member is not None

    def _manual_command_string(self):
        """The command to create a card when an `autocard` is disabled.

        Returns:
            str: the command string corresponding to manual card creation
                when `autocard` is disabled for a `Subscription`.
        """
        return 'gello create_card'
