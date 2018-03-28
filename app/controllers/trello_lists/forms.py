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

"""lists/forms.py

List-related forms.
"""

from flask_wtf import Form
from wtforms import BooleanField, SubmitField


class ListForm(Form):
    """Form for creating a new subscription."""
    active = BooleanField('Active')
    submit = SubmitField('Update')
