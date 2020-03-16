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

"""boards/views.py

Boards-related routes and view-specific logic.
"""

from os import environ
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from . import board
from .forms import RefreshForm
from ...models import Board
from ...services import BoardService

board_service = BoardService()


@board.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """Updates the boards and corresponding lists saved on POST request."""
    if board_service.trello_service.init_if_needed():
        form = RefreshForm()
        if form.validate_on_submit():
            board_service.fetch()
            flash('The boards have been updated.')

            return redirect(url_for('.index'))

        page = request.args.get('page', 1, type=int)
        query = Board.query
        pagination = query.order_by(Board.timestamp.desc()).paginate(
            page, per_page=10,
            error_out=False
        )
        boards = pagination.items

        return render_template(
            'boards.html',
            boards=boards,
            form=form,
            pagination=pagination,
            organization_name=environ.get('GITHUB_ORG_LOGIN')
        )
    else:
        return redirect(url_for('onboarding.index'))
