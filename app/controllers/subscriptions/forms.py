# -*- coding: utf-8 -*-

"""subscriptions/forms.py

Subscription-related forms.
"""

from flask_wtf import Form
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import Required, Length


class NewSubscriptionForm(Form):
    """Form for creating a new subscription."""

    repo_id = StringField(
        'Repo ID',
        validators=[Required(), Length(1, 64)]
    )
    board_id = StringField(
        'Board ID',
        validators=[Required(), Length(1, 64)]
    )
    autocard = BooleanField('Autocard')
    submit = SubmitField('Submit')
