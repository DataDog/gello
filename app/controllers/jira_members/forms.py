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

"""jira_members/forms.py

JIRAMember-related forms.
"""

from flask_wtf import FlaskForm
from wtforms import SubmitField


class RefreshForm(FlaskForm):
    """On submitting the form, fetch and update stored JIRA members."""
    submit = SubmitField(
        'Refresh JIRA Members',
        description='Inserts or updates JIRA members from the JIRA API'
    )
