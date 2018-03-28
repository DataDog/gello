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

"""forms.py

Contributor-related forms.
"""

from flask_wtf import Form
from wtforms import SubmitField


class RefreshForm(Form):
    """"""
    submit = SubmitField('Refresh contributors')
