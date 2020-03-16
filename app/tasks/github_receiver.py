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

from . import GitHubBaseTask
from . import CreateIssueCard, CreatePullRequestCard, CreateManualCard, \
    DeleteCardObjectFromDatabase, CreateIssueIssue, CreatePullRequestIssue, \
    DeleteJIRAIssueObjectFromDatabase, CreateManualIssue
from ..models import Subscription, GitHubMember, Repo, Issue, PullRequest
from config import Config
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
            label_name = Config.REPO_LABELS[repo.name]
        except KeyError:
            label_name = None

        # Perform an action for each of the subscribed lists belonging to a
        # subscription
        for subscription in subscriptions:
            for trello_list in subscription.subscribed_lists:

                # add language label based on repo name (hardcoded)
                label_id = TrelloService()\
                    .get_label_id(subscription.board_id, label_name)

                self._handle_card(
                    board_id=subscription.board_id,
                    list_id=trello_list.list_id,
                    issue_autocard=subscription.issue_autocard,
                    pull_request_autocard=subscription.pull_request_autocard,
                    label_id=label_id,
                    assignee_id=trello_list.trello_member_id
                )
            for jira_project in subscription.subscribed_jira_projects:
                self._handle_jira_issue(
                    project_key=jira_project.subscription_project_key,
                    issue_autocard=subscription.issue_autocard,
                    pull_request_autocard=subscription.pull_request_autocard,
                    label_name=label_name,
                    jira_member_id=jira_project.jira_member_id,
                    issue_type=jira_project.issue_type_id
                )

            for jira_issue_sub in subscription.subscribed_jira_issues:
                self._handle_jira_issue(
                    project_key=jira_issue_sub.subscription_project_key,
                    issue_autocard=subscription.issue_autocard,
                    pull_request_autocard=subscription.pull_request_autocard,
                    label_name=label_name,
                    jira_member_id=jira_issue_sub.jira_member_id,
                    parent_issue=jira_issue_sub.jira_issue_key,
                    issue_type=jira_issue_sub.issue_type_name
                )

    def _handle_jira_issue(self, project_key, issue_autocard,
                           pull_request_autocard, label_name, jira_member_id,
                           parent_issue=None, issue_type=None):
        """Determines which JIRA issue task to enqueue based on the payload
        parameters.

        Args:
            project_key (str): The key of the project to raise an issue on
            issue_autocard (Boolean): If `autocard` is `true` for Issues
                created.
            pull_request_autocard (Boolean): If `autocard` is `true` for Pull
                Requests created.
            label_name (str): The name of the auto-generated label
            jira_member_id (str): The user id for the JIRA Issue assignee.
            parent_issue (str): The key of the parent issue for this sub-issue
            issue_type (str): The id of the issue type of the project

        Returns:
            None
        """
        scope = self.get_scope()
        action = self.payload['action']

        if not issue_autocard and scope == 'issue' and \
            'comment' in self.payload and action == 'created' and \
            self._manual_command_string() in self.payload['comment']['body']:
            self._create_manual_issue(project_key, label_name, jira_member_id,
                                      parent_issue, issue_type)
        if not pull_request_autocard and scope == 'pull_request' and \
            'comment' in self.payload and action == 'created' and \
            self._manual_command_string() in self.payload['comment']['body']:
            self._create_manual_issue(project_key, label_name, jira_member_id,
                                      parent_issue, issue_type)
        if issue_autocard and scope == 'issue' and action == 'opened':
            self._create_jira_issue_issue(project_key, label_name,
                                          jira_member_id,
                                          parent_issue, issue_type)

        elif pull_request_autocard and scope == 'pull_request' \
            and action == 'opened':
            self._create_jira_pull_request_issue(
                project_key, label_name, jira_member_id, parent_issue,
                issue_type)
        elif scope == 'issue' and action == 'closed':
            self._delete_issue_jira_issue_objects()
        elif scope == 'pull_request' and action == 'closed':
            self._delete_pull_request_jira_issue_objects()
        else:
            print('Unsupported event action.')

    def _handle_card(self, board_id, list_id, issue_autocard,
                     pull_request_autocard, label_id, assignee_id):
        """Determines which trello card task to enqueue based on the payload
        parameters.

        Args:
            board_id (str): The id of the board the card will be created on.
            list_id (str): The id of the list the card will be created on.
            issue_autocard (Boolean): If `autocard` is `true` for Issues
                created.
            pull_request_autocard (Boolean): If `autocard` is `true` for Pull
                Requests created.
            label_id (str): The id of the repo-specific language label.
            assignee_id (str): The trello_member_id for the card assignee.

        Returns:
            None
        """
        scope = self.get_scope()
        action = self.payload['action']

        if not issue_autocard and scope == 'issue' and \
           'comment' in self.payload and action == 'created' and \
           self._manual_command_string() in self.payload['comment']['body']:
            self._create_manual_card(board_id, list_id, label_id, assignee_id)
        elif not pull_request_autocard and scope == 'pull_request' and \
             'comment' in self.payload and action == 'created' and \
             self._manual_command_string() in self.payload['comment']['body']:
            self._create_manual_card(board_id, list_id, label_id, assignee_id)
        elif issue_autocard and scope == 'issue' and action == 'opened':
            self._create_trello_issue_card(board_id, list_id, label_id, assignee_id)
        elif pull_request_autocard and scope == 'pull_request' and \
             action == 'opened':
            self._create_trello_pull_request_card(board_id, list_id, label_id, assignee_id)
        elif scope == 'issue' and action == 'closed':
            self._delete_issue_trello_card_objects()
        elif scope == 'pull_request' and action == 'closed':
            self._delete_pull_request_trello_card_objects()
        else:
            print('Unsupported event action.')

    def _create_manual_issue(
        self, project_key, label_name, jira_member_id, parent_issue, issue_type
    ):
        """Creates a task to create a JIRA Issue.

        NOTE: It does not create a card if the user DOES NOT belong to the
        GitHub organization associated with the `GITHUB_ORG_LOGIN`.

        Args:
            project_key (str): The key of the project to raise an issue on
            label_name (str): The name of the auto-generated label
            jira_member_id (str): The user id for the JIRA Issue assignee.
            parent_issue (str): The key of the parent issue for this sub-issue
            (if a sub-issue is to be created)
            issue_type (str): The id of the issue type of the project

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
            label_name=label_name
        )

    def _create_manual_card(self, board_id, list_id, label_id, assignee_id):
        """Creates a task to create a trello card.

        NOTE: It does not create a card if the user DOES NOT belong to the
        GitHub organization associated with the `GITHUB_ORG_LOGIN`.

        Args:
            board_id (str): The id of the board the card will be created on.
            list_id (str): The id of the list the card will be created on.
            label_id (str): The id of the repo-specific language label.
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
            label_id=label_id,
            assignee_id=assignee_id
        )

    def _create_jira_issue_issue(
        self, project_key, label_name, jira_member_id, parent_issue, issue_type
    ):
        """Creates a task to create a JIRA issue for the corresponding GitHub issue.

        NOTE: It does not create a JIRA issue if the user belongs to the GitHub
        organization associated with the `GITHUB_ORG_LOGIN`.

        Args:
            project_key (str): The key of the project to raise an issue on
            label_name (str): The name of the auto-generated label
            jira_member_id (str): The user id for the JIRA Issue assignee.
            parent_issue (str): The key of the parent issue for this sub-issue
            (if a sub-issue is to be created)
            issue_type (str): The id of the issue type of the project

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
            label_name=label_name
        )

    def _create_jira_pull_request_issue(
        self, project_key, label_name, jira_member_id, parent_issue, issue_type
    ):
        """Creates a task to create a JIRA issue for the corresponding GitHub pull
        request.

        NOTE: It does not create a JIRA issue if the user belongs to the GitHub
        organization associated with the `GITHUB_ORG_LOGIN`.

        Args:
            project_key (str): The key of the project to raise an issue on
            label_name (str): The name of the auto-generated label
            jira_member_id (str): The user id for the JIRA Issue assignee.
            parent_issue (str): The key of the parent issue for this sub-issue
            (if a sub-issue is to be created)
            issue_type (str): The id of the issue type of the project

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
            label_name=label_name
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

    def _create_trello_issue_card(self, board_id, list_id, label_id, assignee_id):
        """Creates a task to create a trello card.

        NOTE: It does not create a card if the user belongs to the GitHub
        organization associated with the `GITHUB_ORG_LOGIN`.

        Args:
            board_id (str): The id of the board the card will be created on.
            list_id (str): The id of the list the card will be created on.
            label_id (str): The id of the repo-specific language label.
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
            label_id=label_id,
            assignee_id=assignee_id
        )

    def _create_trello_pull_request_card(self, board_id, list_id, label_id, assignee_id):
        """Creates a task to create a trello card.

        NOTE: It does not create a card if the user belongs to the GitHub
        organization associated with the `GITHUB_ORG_LOGIN`.

        Args:
            board_id (str): The id of the board the card will be created on.
            list_id (str): The id of the list the card will be created on.
            label_id (str): The id of the repo-specific language label.
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
            label_id=label_id,
            assignee_id=assignee_id
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
            DeleteCardObjectFromDatabase.delay(
                scope=scope,
                github_id=github_id
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
            DeleteCardObjectFromDatabase.delay(
                scope=scope,
                github_id=github_id
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
