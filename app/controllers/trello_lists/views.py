# -*- coding: utf-8 -*-

"""lists/views.py

lists-related routes and view-specific logic.
"""

from flask import render_template, request, current_app
from flask.ext.login import login_required
from . import trello_list
from ...models import Board, List


@trello_list.route('/<int:id>', methods=['GET'])
@login_required
def index(id):
    """
    Displays trello lists pertaining to a particular board.
    """
    board = Board.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)

    pagination = board.lists.order_by(List.timestamp.asc()).paginate(
        page, per_page=10, error_out=False
    )
    lists = pagination.items

    return render_template(
        'trello_lists.html',
        board=board,
        lists=lists,
        pagination=pagination
    )
