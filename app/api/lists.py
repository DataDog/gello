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

"""api/lists.py

Exposed lists for autocomplete.
"""

from flask import jsonify, request, url_for
from flask_login import login_required
from ..models import List
from . import api


@api.route('/lists/<string:board_id>')
@login_required
def get_lists(board_id):
    list = request.args.get('list', 1, type=int)

    pagination = List.query.filter_by(board_id=board_id).paginate(
        list, per_page=100, error_out=False)
    lists = pagination.items

    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_lists', list=list-1, _external=True)

    next = None
    if pagination.has_next:
        next = url_for('api.get_lists', list=list+1, _external=True)

    return jsonify(
        {
            'lists': [list.to_json() for list in lists],
            'prev': prev,
            'next': next,
            'count': pagination.total
        }
    )
