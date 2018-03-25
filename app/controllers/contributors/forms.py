# -*- coding: utf-8 -*-

"""forms.py

Contributor-related forms.
"""

from flask_wtf import Form
from wtforms import SubmitField


class RefreshForm(Form):
    """"""
    submit = SubmitField('Refresh contributors')
