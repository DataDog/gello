# -*- coding: utf-8 -*-

"""subscriptions/views.py

subscriptions-related routes and view-specific logic.
"""

from flask import render_template, redirect, url_for, flash, request,\
    current_app
from flask_login import login_required
from . import subscription
from .forms import NewSubscriptionForm
from ... import db
from ...models import Subscription


@subscription.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """Updates the repositories saved on POST request."""
    form = NewSubscriptionForm()
    page = request.args.get('page', 1, type=int)
    query = Subscription.query
    pagination = query.order_by(Subscription.timestamp.desc()).paginate(
        page, per_page=10,
        error_out=False
    )
    subscriptions = pagination.items

    return render_template(
        'subscriptions.html',
        subscriptions=subscriptions,
        form=form,
        pagination=pagination
    )


@subscription.route('/create', methods=['POST'])
@login_required
def create():
    """Creates a new subscription."""
    flash('Created subscription')
    return redirect(url_for('.index'))


@subscription.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    """Deletes an old subscription."""
    # id is a string "{board_id}|{repo_id}"
    # TODO: split the string
    flash('Deleted subscription')
    return redirect(url_for('.index'))
