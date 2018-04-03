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

"""boards/forms.py

Board-related forms.
"""

from flask_wtf import FlaskForm
from wtforms import SubmitField


class RefreshForm(FlaskForm):
    """Refreshes boards from the Trello API when submitted."""
    submit = SubmitField(
        'Refresh boards',
        description='Inserts or updates Trello boards from the Trello API'
    )
