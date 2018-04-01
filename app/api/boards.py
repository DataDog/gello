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

"""api/boards.py

Exposed boards for autocomplete.
"""

from flask import jsonify, request, url_for
from flask_login import login_required
from ..models import Board
from . import api


@api.route('/boards/')
@login_required
def get_boards():
    board = request.args.get('board', 1, type=int)

    pagination = Board.query.paginate(board, per_page=100, error_out=False)
    boards = pagination.items

    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_boards', board=board-1, _external=True)

    next = None
    if pagination.has_next:
        next = url_for('api.get_boards', board=board+1, _external=True)

    return jsonify(
        {
            'boards': [board.to_json() for board in boards],
            'prev': prev,
            'next': next,
            'count': pagination.total
        }
    )
