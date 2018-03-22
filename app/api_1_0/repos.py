# -*- coding: utf-8 -*-

"""repos.py

Methods for mutating GitHub repositories
TODO: add a way to create webhooks from the repository.
"""

from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..models import Repo
from . import api


@api.route('/repos/')
def get_repos():
    page = request.args.get('page', 1, type=int)
    pagination = Repo.query.paginate(
        page,
        per_page=10,
        error_out=False
    )
    repos = pagination.items

    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_repos', page=page-1, _external=True)

    next = None
    if pagination.has_next:
        next = url_for('api.get_repos', page=page+1, _external=True)

    return jsonify({
        'repos': [repo.to_json() for repo in repos],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/repos/<int:id>')
def get_repo(id):
    repo = Repo.query.get_or_404(id)

    return jsonify(repo.to_json())


@api.route('/repos/', methods=['POST'])
def new_repo():
    repo = Repo.from_json(request.json)
    db.session.add(repo)
    db.session.commit()

    return jsonify(repo.to_json()), 201, \
        {'Location': url_for('api.get_repo', id=repo.id, _external=True)}


@api.route('/repos/<int:id>', methods=['PUT'])
def edit_repo(id):
    repo = Repo.query.get_or_404(id)
    db.session.add(repo)

    return jsonify(repo.to_json())
