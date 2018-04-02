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
from wtforms import StringField, BooleanField, SubmitField, IntegerField
from wtforms.validators import Required, Length
from ...models import List


class NewSubscriptionForm(Form):
    """Form for creating a new subscription."""
    board_id = StringField(
        'Board ID',
        validators=[Required(), Length(1, 64)],
        description=textwrap.dedent(
            """
            The <code>id</code> of a trello board you wish to subscribe
            """
        )
    )
    repo_id = IntegerField(
        'Repo ID',
        validators=[Required()],
        description=textwrap.dedent(
            """
            The <code>id</code> of a github repository board you wish to
            register event webhooks for
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

    def validate(self):
        """Validates the list_ids attribute is correct."""
        ids = self.list_ids.data.strip()

        # If the field is empty, return `True`
        if not ids:
            return True

        ids_list = re.split("\s*,\s*", ids)

        return all(
            List.query.filter_by(
                trello_list_id=list_id, board_id=self.board_id.data
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
