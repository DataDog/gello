# -*- coding: utf-8 -*-

"""lists/views.py

lists-related routes and view-specific logic.
"""

from flask import render_template, request, current_app
from flask_login import login_required
from . import trello_list
from ...models import Board, List


@trello_list.route('/<int:id>', methods=['GET'])
@login_required
def index(id):
    """
    Displays trello lists pertaining to a particular board.
    """
    board = Board.query.get_or_404(id)
    lists = board.lists.order_by(List.timestamp.asc())

    return render_template(
        'trello_lists.html',
        board=board,
        lists=lists
    )
