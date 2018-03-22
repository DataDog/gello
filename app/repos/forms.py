# -*- coding: utf-8 -*-

"""forms.py
"""

from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from flask.ext.pagedown.fields import PageDownField


class RepoForm(Form):
    """"""
    body = PageDownField("What's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')
