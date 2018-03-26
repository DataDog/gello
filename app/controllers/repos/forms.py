# -*- coding: utf-8 -*-

"""forms.py

Repository-related forms.
"""

from flask_wtf import Form
from wtforms import SubmitField


class RefreshForm(Form):
    """"""
    submit = SubmitField('Refresh repositories')
