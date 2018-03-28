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

"""issues/views.py

issues-related routes and view-specific logic.
"""

from flask import render_template, request
from flask_login import login_required
from . import issue
from ...models import Repo, Issue


@issue.route('/<int:id>', methods=['GET'])
@login_required
def index(id):
    """
    Displays issues opened by external contributors related to a repository.
    """
    repo = Repo.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)

    pagination = repo.issues.order_by(Issue.timestamp.asc()).paginate(
        page, per_page=10, error_out=False
    )
    issues = pagination.items

    return render_template(
        'issues.html',
        repo=repo,
        issues=issues,
        pagination=pagination
    )
