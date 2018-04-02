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

"""subscribed_lists/forms.py

SubscribedList-related forms.
"""

import textwrap

from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length
from ...models import List


class NewForm(Form):
    """Form for creating a subscribed_list."""
    list_id = StringField(
        'List ID',
        validators=[Required(), Length(1, 64)],
        description=textwrap.dedent(
            """
            The <code>id</code> of a trello list associated with the trello
            board subscribed
            """
        )
    )
    trello_member_id = StringField(
        'Trello Member ID',
        description=textwrap.dedent(
            """
            An optional <code>id</code> for a member to be automatically
            assigned to any trello cards created on this list
            """
        )
    )
    submit = SubmitField('Create')

    def __init__(self, board_id):
        """Sets the `board_id` for the form."""
        Form.__init__(self)
        self._board_id = board_id

    def validate(self):
        """Validates the list_id attribute is correct."""
        list_id = self.list_id.data

        return List.query.filter_by(
            trello_list_id=list_id, board_id=self._board_id
        ).first() is not None


class DeleteForm(Form):
    """Form for deleting an existing subscribed_list."""
    submit = SubmitField('Delete')
