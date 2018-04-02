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

"""github_members/forms.py

GitHubMember-related forms.
"""

from flask_wtf import Form
from wtforms import SubmitField


class RefreshForm(Form):
    """On submitting the form, fetch and update stored github members."""
    submit = SubmitField(
        'Refresh GitHub Members',
        description='Inserts or updates GitHub members from the GitHub API'
    )
