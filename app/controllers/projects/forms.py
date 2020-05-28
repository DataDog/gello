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

"""projects/forms.py

Project-related forms (JIRA).
"""

from flask_wtf import FlaskForm
from wtforms import SubmitField


class RefreshForm(FlaskForm):
    """Refreshes projects and Users from the JIRA API when submitted."""
    submit = SubmitField(
        'Refresh projects and JIRA members',
        description='Inserts or updates JIRA projects and members from the JIRA API'
    )
