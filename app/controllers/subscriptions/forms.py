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

"""subscriptions/forms.py

Subscription-related forms.
"""

import re
import textwrap

from flask_wtf import Form
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import Required, Length
from ...models import Board, List, Repo


class NewSubscriptionForm(Form):
    """Form for creating a new subscription."""
    board_name = StringField(
        'Board Name',
        validators=[Required(), Length(1, 100)],
        description=textwrap.dedent(
            """
            The name of a Trello board you wish to subscribe
            """
        )
    )
    repo_name = StringField(
        'Repo Name',
        validators=[Required(), Length(1, 100)],
        description=textwrap.dedent(
            """
            The name of a GitHub repository you wish to register event webhooks
            for
            """
        )
    )
    list_ids = StringField(
        'List IDs',
        description=textwrap.dedent(
            """
            A comma delimited list of <code>List.trello_list_id</code>s
            belonging to the <code>Board</code> associated with the
            <code>board_id</code> above
            """
        )
    )
    issue_autocard = BooleanField(
        'Issue Autocard',
        description=textwrap.dedent(
            """
            If checked, trello cards will automatically be created when a
            contributor outside of your organization submits a
            <a href='https://help.github.com/articles/about-issues/'>GitHub
            Issue</a>.
            """
        )
    )
    pull_request_autocard = BooleanField(
        'Pull Request Autocard',
        description=textwrap.dedent(
            """
            If checked, trello cards will automatically be created when a
            contributor outside of your organization submits a
            <a href='https://help.github.com/articles/about-pull-requests/'>
            Pull Request</a>.
            """
        )
    )
    submit = SubmitField('Create')

    def get_board_id(self):
        return self._board_id

    def get_repo_id(self):
        return self._repo_id

    def validate(self):
        """Performs validations of the form field values.

        - Validates the `board_id `attribute belongs to a `Board`
        - Validates the `repo_id `attribute belongs to a `Repo`
        - Validates the `list_ids` attribute is a comma-delimited list of
          `List.trello_list_id` belonging to the `Board` with `board_id`.
        """
        board_name = self.board_name.data.strip()
        repo_name = self.repo_name.data.strip()
        ids = self.list_ids.data.strip()

        # Perform board-specific validations
        board = Board.query.filter_by(name=board_name).first()
        if board is None:
            return False
        self._board_id = board.trello_board_id

        # Perform repo-specific validations
        repo = Repo.query.filter_by(name=repo_name).first()
        if repo is None:
            return False
        self._repo_id = repo.github_repo_id

        # If the field is empty, return `True`
        if not ids:
            return True

        ids_list = re.split("\s*,\s*", ids)

        return all(
            List.query.filter_by(
                trello_list_id=list_id, board_id=self.get_board_id()
            ) is not None for list_id in ids_list
        )


class UpdateForm(Form):
    """Form for updating an existing subscription."""
    issue_autocard = BooleanField('Issue Autocard')
    pull_request_autocard = BooleanField('Pull Request Autocard')
    submit = SubmitField('Update')


class DeleteForm(Form):
    """Form for deleting an existing subscription."""
    submit = SubmitField('Delete')
