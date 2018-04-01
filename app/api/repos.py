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

"""api/repos.py

Exposed repos for autocomplete.
"""

from flask import jsonify, request, url_for
from flask_login import login_required
from ..models import Repo
from . import api


@api.route('/repos/')
@login_required
def get_repos():
    repo = request.args.get('repo', 1, type=int)

    pagination = Repo.query.paginate(repo, per_page=100, error_out=False)
    repos = pagination.items

    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_repos', repo=repo-1, _external=True)

    next = None
    if pagination.has_next:
        next = url_for('api.get_repos', repo=repo+1, _external=True)

    return jsonify(
        {
            'repos': [repo.to_json() for repo in repos],
            'prev': prev,
            'next': next,
            'count': pagination.total
        }
    )
