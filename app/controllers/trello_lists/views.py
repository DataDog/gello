# -*- coding: utf-8 -*-

"""lists/views.py

lists-related routes and view-specific logic.
"""

from flask import render_template, request, current_app, flash, redirect,\
    url_for
from flask_login import login_required
from . import trello_list
from .forms import ListForm
from ...models import Board, List
from ... import db


@trello_list.route('/<int:id>', methods=['GET'])
@login_required
def index(id):
    """
    Displays trello lists pertaining to a particular board.
    """
    board = Board.query.get_or_404(id)
    lists = board.lists.order_by(List.timestamp.asc())
    list_form_pairs = [(l, ListForm(active=l.active)) for l in lists]

    return render_template(
        'trello_lists.html',
        board=board,
        list_form_pairs=list_form_pairs
    )


@trello_list.route('/<int:board_id>/update/<int:list_id>', methods=['POST'])
@login_required
def update(board_id, list_id):
    """Update a trello list."""
    form = ListForm(request.form)

    if form.active.data is not None:
        trello_list = List.query.get(list_id)
        trello_list.active = form.active.data

        # persist the changes
        db.session.commit()
        flash('The list has been updated')
    else:
        flash('ERROR The list has NOT been updated.')

    return redirect(url_for('.index', id=board_id))
