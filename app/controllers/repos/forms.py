# -*- coding: utf-8 -*-

"""forms.py

Repository-related forms.
"""

from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField


class RepoForm(Form):
    """"""
    submit = SubmitField('Submit')


class RefreshForm(Form):
    """"""
    submit = SubmitField('Refresh repositories')
