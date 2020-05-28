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

"""lists/views.py

lists-related routes and view-specific logic.
"""

from flask import render_template, redirect, url_for
from flask_login import login_required
from . import trello_list
from ...models import Board, List, ConfigValue


@trello_list.route('/<int:id>', methods=['GET'])
@login_required
def index(id):
    """
    Displays trello lists pertaining to a particular board.
    """

    if not ConfigValue.query.get('TRELLO_ORG_NAME'):
        return redirect(url_for('onboarding.index'))

    board = Board.query.get_or_404(id)
    lists = board.lists.order_by(List.timestamp.asc())

    return render_template(
        'trello_lists.html',
        board=board,
        lists=lists
    )
