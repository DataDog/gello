# -*- coding: utf-8 -*-

"""boards/views.py

Boards-related routes and view-specific logic.
"""

from flask import render_template, redirect, url_for, flash, request,\
    current_app
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
    form = RefreshForm()
    if form.validate_on_submit():
        board_service.create_or_update_boards()
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


@board.route('/repos/<int:id>', methods=['GET', 'POST'])
@login_required
def repos(int):
    """Lists the repositories associated with a Trello board."""
    # TODO: add form for adding new repositories (include github id, or something)
    # Add subscription association (repo_id, and board_id, and autocard boolean)
    # class Subscription(db.Model):
    #     __tablename__ = 'subscriptions'
    #     repo_id
    #     board_id
    #     autocard
    pass
