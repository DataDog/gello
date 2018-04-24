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

from app import db
from mock import patch
from app.tasks import GitHubReceiver, CreateIssueCard, CreatePullRequestCard, \
    CreateManualCard, DeleteCardObjectFromDatabase
from tests.utils import create_board, create_repo, create_list, \
    create_subscription, create_subscribed_list, json_fixture, create_issue
from tests.base_test_case import BaseTestCase


class PatchClass:
    """A class used to patch methods in the `GitHubReceiver`."""

    def user_not_in_org(self):
        return False

    def user_in_org(self):
        return True


class GitHubReceiverAutocardTestCase(BaseTestCase):
    """Tests the `GitHubReceiver` celery task for `autocard` settings."""

    def setUp(self):
        """Sets up testing context."""
        super().setUp()
        create_board()
        create_repo()
        create_list()
        create_subscription(issue_autocard=True, pull_request_autocard=True)
        create_subscribed_list()
        db.session.commit()

    @patch(
        'app.tasks.GitHubReceiver._user_in_organization',
        new=PatchClass.user_not_in_org
    )
    @patch.object(CreateIssueCard, 'delay')
    def test_issue_opened_by_external_contributor(self, mock):
        """Tests `CreateIssueCard` is enqueued."""
        payload = json_fixture('./tests/fixtures/issue_opened.json')
        GitHubReceiver.delay(payload=payload)
        mock.assert_called_once()

    @patch(
        'app.tasks.GitHubReceiver._user_in_organization',
        new=PatchClass.user_in_org
    )
    @patch.object(CreateIssueCard, 'delay')
    def test_issue_opened_by_organization_member(self, mock):
        """Tests `CreateIssueCard` is not enqueued."""
        payload = json_fixture('./tests/fixtures/issue_opened.json')
        GitHubReceiver.delay(payload=payload)
        mock.assert_not_called()

    @patch(
        'app.tasks.GitHubReceiver._user_in_organization',
        new=PatchClass.user_not_in_org
    )
    @patch.object(CreatePullRequestCard, 'delay')
    def test_pull_request_opened_by_external_contributor(self, mock):
        """Tests `CreatePullRequestCard` is enqueued."""
        payload = json_fixture('./tests/fixtures/pull_request_opened.json')
        GitHubReceiver.delay(payload=payload)
        mock.assert_called_once()

    @patch(
        'app.tasks.GitHubReceiver._user_in_organization',
        new=PatchClass.user_in_org
    )
    @patch.object(CreatePullRequestCard, 'delay')
    def test_pull_request_opened_by_organization_member(self, mock):
        """Tests `CreatePullRequestCard` is not enqueued."""
        payload = json_fixture('./tests/fixtures/pull_request_opened.json')
        GitHubReceiver.delay(payload=payload)
        mock.assert_not_called()

    @patch(
        'app.tasks.GitHubReceiver._user_in_organization',
        new=PatchClass.user_not_in_org
    )
    @patch.object(CreateManualCard, 'delay')
    def test_manual_command_by_external_contributor(self, mock):
        """Tests `CreateManualCard` is not enqueued."""
        payload = json_fixture('./tests/fixtures/manual_comment.json')
        GitHubReceiver.delay(payload=payload)
        mock.assert_not_called()

    @patch(
        'app.tasks.GitHubReceiver._user_in_organization',
        new=PatchClass.user_in_org
    )
    @patch.object(CreateManualCard, 'delay')
    def test_manual_command_by_organization_member(self, mock):
        """Tests `CreateManualCard` is not enqueued."""
        payload = json_fixture('./tests/fixtures/manual_comment.json')
        GitHubReceiver.delay(payload=payload)
        mock.assert_not_called()

    @patch(
        'app.tasks.GitHubReceiver._user_in_organization',
        new=PatchClass.user_not_in_org
    )
    @patch.object(DeleteCardObjectFromDatabase, 'delay')
    def test_closed_event(self, mock):
        """Tests `DeleteCardObjectFromDatabase` is enqueued."""
        create_issue()
        payload = json_fixture('./tests/fixtures/issue_closed.json')
        GitHubReceiver.delay(payload=payload)
        mock.assert_called_once()


class GitHubReceiverManualTestCase(BaseTestCase):
    """Tests the `GitHubReceiver` celery task for `autocard` settings."""

    def setUp(self):
        """Sets up testing context."""
        super().setUp()
        create_board()
        create_repo()
        create_list()
        create_subscription(issue_autocard=False, pull_request_autocard=False)
        create_subscribed_list()
        db.session.commit()

    @patch(
        'app.tasks.GitHubReceiver._user_in_organization',
        new=PatchClass.user_not_in_org
    )
    @patch.object(CreateIssueCard, 'delay')
    def test_issue_opened_by_external_contributor(self, mock):
        """Tests that the `CreateIssueCard` is not enqueued."""
        payload = json_fixture('./tests/fixtures/issue_opened.json')
        GitHubReceiver.delay(payload=payload)

        # It does not enqueue the `CreateIssueCard` task
        mock.assert_not_called()

    @patch(
        'app.tasks.GitHubReceiver._user_in_organization',
        new=PatchClass.user_in_org
    )
    @patch.object(CreateIssueCard, 'delay')
    def test_issue_opened_by_organization_member(self, mock):
        """Tests that the `CreateIssueCard` is not enqueued."""
        payload = json_fixture('./tests/fixtures/issue_opened.json')
        GitHubReceiver.delay(payload=payload)

        # It does not enqueue the `CreateIssueCard` task
        mock.assert_not_called()

    @patch(
        'app.tasks.GitHubReceiver._user_in_organization',
        new=PatchClass.user_not_in_org
    )
    @patch.object(CreatePullRequestCard, 'delay')
    def test_pull_request_opened_by_external_contributor(self, mock):
        """Tests that the `CreatePullRequestCard` is not enqueued."""
        payload = json_fixture('./tests/fixtures/pull_request_opened.json')
        GitHubReceiver.delay(payload=payload)

        # It does not enqueue the `CreatePullRequestCard` task
        mock.assert_not_called()

    @patch(
        'app.tasks.GitHubReceiver._user_in_organization',
        new=PatchClass.user_in_org
    )
    @patch.object(CreatePullRequestCard, 'delay')
    def test_pull_request_opened_by_organization_member(self, mock):
        """Tests that the `CreatePullRequestCard` is not enqueued."""
        payload = json_fixture('./tests/fixtures/pull_request_opened.json')
        GitHubReceiver.delay(payload=payload)

        # It does not enqueue the `CreatePullRequestCard` task
        mock.assert_not_called()

    @patch(
        'app.tasks.GitHubReceiver._user_in_organization',
        new=PatchClass.user_not_in_org
    )
    @patch.object(CreateManualCard, 'delay')
    def test_manual_command_by_external_contributor(self, mock):
        """Tests `CreateManualCard` is enqueued."""
        payload = json_fixture('./tests/fixtures/manual_comment.json')
        GitHubReceiver.delay(payload=payload)
        mock.assert_not_called()

    @patch(
        'app.tasks.GitHubReceiver._user_in_organization',
        new=PatchClass.user_in_org
    )
    @patch.object(CreateManualCard, 'delay')
    def test_manual_command_by_organization_member(self, mock):
        """Tests `CreateManualCard` is enqueued."""
        payload = json_fixture('./tests/fixtures/manual_comment.json')
        GitHubReceiver.delay(payload=payload)
        mock.assert_called_once()

    @patch(
        'app.tasks.GitHubReceiver._user_in_organization',
        new=PatchClass.user_not_in_org
    )
    @patch.object(DeleteCardObjectFromDatabase, 'delay')
    def test_closed_event(self, mock):
        """Tests `DeleteCardObjectFromDatabase` is enqueued."""
        create_issue()
        payload = json_fixture('./tests/fixtures/issue_closed.json')
        GitHubReceiver.delay(payload=payload)
        mock.assert_called_once()
