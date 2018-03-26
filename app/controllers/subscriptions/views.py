# -*- coding: utf-8 -*-

"""subscriptions/views.py

subscriptions-related routes and view-specific logic.
"""

from flask import render_template, redirect, url_for, flash, request,\
    current_app
from flask_login import login_required
from . import subscription
from .forms import NewSubscriptionForm
from ...models import Subscription
from ...services import SubscriptionService

subscription_service = SubscriptionService()


@subscription.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """Updates the repositories saved on POST request."""
    # Creation form logic
    create_form = NewSubscriptionForm()
    if create_form.validate_on_submit():
        subscription_service.create(
            board_id=create_form.board_id.data,
            repo_id=int(create_form.repo_id.data), # TODO some sort of type checking before this
            autocard=create_form.autocard.data
        )
        flash('Created subscription')
        return redirect(url_for('.index'))

    # delete_form = DeleteSubscriptionForm()
    # flash('Deleted subscription')
    # return redirect(url_for('.index'))

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
        form=create_form,
        pagination=pagination
    )
