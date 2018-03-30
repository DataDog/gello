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

from flask_wtf import Form
from wtforms import StringField, BooleanField, SubmitField, IntegerField
from wtforms.validators import Required, Length
from ...models import List


class NewSubscriptionForm(Form):
    """Form for creating a new subscription."""

    board_id = StringField(
        'Board ID',
        validators=[Required(), Length(1, 64)]
    )
    repo_id = IntegerField(
        'Repo ID',
        validators=[Required()]
    )
    list_ids = StringField('List IDs')
    autocard = BooleanField('Autocard')
    submit = SubmitField('Create')

    def validate(self):
        """Validates the list_ids attribute is correct."""
        ids = self.list_ids.data
        ids_list = re.split("\s*,\s*", ids)

        # TODO: try to do this is one query
        return all(
            List.query.filter_by(
                trello_list_id=list_id, board_id=self.board_id.data
            ) is not None for list_id in ids_list
        )


class UpdateForm(Form):
    """Form for updating an existing subscription."""

    autocard = BooleanField('Autocard')
    submit = SubmitField('Update')


class DeleteForm(Form):
    """Form for deleting an existing subscription."""

    submit = SubmitField('Delete')
