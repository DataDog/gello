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

from flask_wtf import Form
from wtforms import StringField, BooleanField, SubmitField, IntegerField
from wtforms.validators import Required, Length


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
    autocard = BooleanField('Autocard')
    submit = SubmitField('Create')


class UpdateForm(Form):
    """Form for updating an existing subscription."""

    autocard = BooleanField('Autocard')
    submit = SubmitField('Update')


class DeleteForm(Form):
    """Form for deleting an existing subscription."""

    submit = SubmitField('Delete')
