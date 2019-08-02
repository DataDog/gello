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

"""api/boards.py

Exposed boards for autocomplete.
"""

from flask import jsonify
from flask_login import login_required
from . import api
from app.services import GitHubService, TrelloService

trello_service = TrelloService()
github_service = GitHubService()


@api.route('/trello_names/')
@login_required
def get_trello_names():
    trello_organizations = trello_service.organizations()

    return jsonify(
        {
            'names': [{'label': o.name} for o in trello_organizations]
        }
    )


@api.route('/github_logins/')
@login_required
def get_github_logins():
    github_organizations = github_service.organizations()

    return jsonify(
        {
            'logins': [{'label': o.login} for o in github_organizations]
        }
    )
