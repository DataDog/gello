# -*- coding: utf-8 -*-

"""contributors/views.py

Contributors-related routes and view-specific logic.
"""

from flask import render_template, redirect, url_for, flash, request,\
    current_app
from flask_login import login_required
from . import contributor
from .forms import RefreshForm
from ...models import Contributor
from ...services import ContributorService

contributor_service = ContributorService()


@contributor.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """Updates the contributors saved on POST request."""
    form = RefreshForm()
    if form.validate_on_submit():
        contributor_service.fetch()
        flash('The organization contributors have been updated.')
        return redirect(url_for('.index'))

    page = request.args.get('page', 1, type=int)
    query = Contributor.query
    pagination = query.order_by(Contributor.login.asc()).paginate(
        page, per_page=10,
        error_out=False
    )
    contributors = pagination.items

    return render_template(
        'contributors.html',
        contributors=contributors,
        form=form,
        pagination=pagination
    )
