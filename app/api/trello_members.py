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

"""api/trello_members.py

Exposed trello_members for autocomplete.
"""

from flask import jsonify, request, url_for
from flask_login import login_required
from ..models import TrelloMember
from . import api


@api.route('/trello_members/')
@login_required
def get_trello_members():
    trello_member = request.args.get('trello_member', 1, type=int)

    pagination = TrelloMember.query.paginate(
        trello_member, per_page=1000, error_out=False
    )
    trello_members = pagination.items

    prev = None
    if pagination.has_prev:
        prev = url_for(
            'api.get_trello_members',
            trello_member=trello_member-1,
            _external=True
        )

    next = None
    if pagination.has_next:
        next = url_for(
            'api.get_trello_members',
            trello_member=trello_member+1,
            _external=True
        )

    return jsonify(
        {
            'trello_members': [tm.to_json() for tm in trello_members],
            'prev': prev,
            'next': next,
            'count': pagination.total
        }
    )
