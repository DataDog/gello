# -*- coding: utf-8 -*-

"""boards/views.py

Boards-related routes and view-specific logic.
"""

from flask import render_template, redirect, url_for, flash, request,\
    current_app
from flask.ext.login import login_required
from . import board
from .forms import RefreshForm
from ... import db
from ...models import Board, List
from ...services import TrelloService


@board.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """Updates the boards and corresponding lists saved on POST request."""
    form = RefreshForm()
    if form.validate_on_submit():
        trello_service = TrelloService()

        # Add all the boards to the Database for the organization
        for b in trello_service.boards():
            _b = Board(name=b.name, url=b.url, trello_board_id=b.id)
            db.session.add(_b)

            # Add all the lists to the Database for a given board
            for l in b.all_lists():
                _l = List(
                    active=False,
                    name=l.name,
                    trello_list_id=l.id,
                    board_id=_b.id
                )
                db.session.add(_l)

        # Persist the boards and lists
        db.session.commit()
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
        pagination=pagination
    )
