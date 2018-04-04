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

"""issues/views.py

issues-related routes and view-specific logic.
"""

from flask import render_template, request
from flask_login import login_required
from . import issue
from ...models import Board, Repo, Issue


@issue.route('/repo/<int:repo_id>', methods=['GET'])
@login_required
def index(repo_id):
    """
    Displays issues opened by external contributors related to a repository.
    """
    repo = Repo.query.get_or_404(repo_id)
    page = request.args.get('page', 1, type=int)

    pagination = repo.issues.order_by(Issue.timestamp.asc()).paginate(
        page, per_page=10, error_out=False
    )
    issues = pagination.items

    return render_template(
        'issues.html',
        repo=repo,
        issues=issues,
        pagination=pagination
    )


@issue.route('/repo/<int:repo_id>/board/<string:board_id>', methods=['GET'])
@login_required
def filtered_by_board(repo_id, board_id):
    """
    Displays issues opened by external contributors related to a repository,
    filtered by a particular `board_id`.
    """
    repo = Repo.query.get_or_404(repo_id)
    board = Board.query.filter_by(trello_board_id=board_id).first()
    page = request.args.get('page', 1, type=int)

    issue_records = Issue.query.filter_by(
        repo_id=repo_id, trello_board_id=board_id
    )
    pagination = issue_records.order_by(Issue.timestamp.asc()).paginate(
        page, per_page=10, error_out=False
    )
    issues = pagination.items

    return render_template(
        'issues.html',
        repo=repo,
        board=board,
        issues=issues,
        pagination=pagination
    )
