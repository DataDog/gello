# -*- coding: utf-8 -*-

"""subscriptions/views.py

subscriptions-related routes and view-specific logic.
"""

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from . import subscription
from .forms import NewSubscriptionForm, UpdateForm, DeleteForm
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
            repo_id=create_form.repo_id.data,
            autocard=create_form.autocard.data
        )
        flash('Created subscription')
        return redirect(url_for('.index'))

    page = request.args.get('page', 1, type=int)
    query = Subscription.query
    pagination = query.order_by(Subscription.timestamp.desc()).paginate(
        page, per_page=10,
        error_out=False
    )
    subscriptions = pagination.items
    subscription_forms_tuples = [(s, UpdateForm(autocard=s.autocard),
                                  DeleteForm()) for s in subscriptions]

    return render_template(
        'subscriptions.html',
        create_form=create_form,
        subscription_forms_tuples=subscription_forms_tuples,
        pagination=pagination
    )


@subscription.route('/<string:board_id>/<int:repo_id>/update', methods=['POST'])
@login_required
def update(board_id, repo_id):
    form = UpdateForm(request.form)

    if form.autocard.data is not None:
        subscription_service.update(
            board_id=board_id,
            repo_id=repo_id,
            autocard=form.autocard.data
        )
        flash('Updated subscription')
    else:
        flash('ERROR The subscription has NOT been updated')

    return redirect(url_for('.index'))


@subscription.route('/<string:board_id>/<int:repo_id>/delete', methods=['POST'])
@login_required
def delete(board_id, repo_id):
    subscription_service.delete(board_id, repo_id)
    flash('Deleted subscription')
    return redirect(url_for('.index'))
