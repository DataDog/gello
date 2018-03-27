# -*- coding: utf-8 -*-

"""lists/forms.py

List-related forms.
"""

from flask_wtf import Form
from wtforms import BooleanField, SubmitField


class ListForm(Form):
    """Form for creating a new subscription."""
    active = BooleanField('Active')
    submit = SubmitField('Update')
