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

from flask import render_template, request, redirect, url_for
from flask_login import login_required
from . import issue
from ...models import Board, Repo, Issue, Project, ConfigValue


@issue.route('/repo/<int:repo_id>/', methods=['GET'])
@login_required
def index(repo_id):
    """
    Displays issues opened by external contributors related to a repository.
    """
    if ConfigValue.query.get('TRELLO_ORG_NAME'):
        repo = Repo.query.get_or_404(repo_id)
        page = request.args.get('page', 1, type=int)

        pagination = repo.issues.filter(
            Issue.jira_issue_key.is_(None)
        ).order_by(Issue.timestamp.asc()).paginate(
            page, per_page=10, error_out=False
        )
        issues = pagination.items

        return render_template(
            'issues.html',
            repo=repo,
            issues=issues,
            board=True,
            jira_base_url=None,
            pagination=pagination
        )
    else:
        return redirect(url_for('onboarding.index'))


@issue.route('/repo/jira/<int:repo_id>/', methods=['GET'])
@login_required
def jira(repo_id):
    """
    Displays issues opened by external contributors related to a repository.
    """
    repo = Repo.query.get_or_404(repo_id)
    if not ConfigValue.get_or_insert_jira_address():
        return render_template(
            '500.html',
            jira_description="No JIRA server found, please set JIRA config values"
        ), 500

    page = request.args.get('page', 1, type=int)

    pagination = repo.issues.filter(
        Issue.jira_issue_key.isnot(None)
    ).order_by(Issue.timestamp.asc()).paginate(
        page, per_page=10, error_out=False
    )
    issues = pagination.items

    return render_template(
        'issues.html',
        repo=repo,
        issues=issues,
        project=True,
        jira_base_url=ConfigValue.get_or_insert_jira_address(),
        pagination=pagination
    )


@issue.route('/repo/<int:repo_id>/board/<string:board_id>', methods=['GET'])
@login_required
def filtered_by_board(repo_id, board_id):
    """
    Displays issues opened by external contributors related to a repository,
    filtered by a particular `board_id`.
    """
    if ConfigValue.query.get('TRELLO_ORG_NAME'):
        repo = Repo.query.get_or_404(repo_id)
        board = Board.query.filter_by(trello_board_id=board_id).first()
        page = request.args.get('page', 1, type=int)

        issue_records = Issue.query.filter_by(
            repo_id=repo.github_repo_id, trello_board_id=board_id
        )
        pagination = issue_records.order_by(Issue.timestamp.asc()).paginate(
            page, per_page=10, error_out=False
        )
        issues = pagination.items

        return render_template(
            'issues.html',
            repo=repo,
            board=board,
            issues=issues,
            pagination=pagination
        )
    else:
        return redirect(url_for('onboarding.index'))


@issue.route('/repo/<int:repo_id>/project/<string:project_key>', methods=['GET'])
@login_required
def filtered_by_project(repo_id, project_key):
    """
    Displays issues opened by external contributors related to a repository,
    filtered by a particular `project_key`.
    """
    if not ConfigValue.get_or_insert_jira_address():
        return render_template(
            '500.html',
            jira_description="No JIRA server found, please set JIRA config values"
        ), 500

    repo = Repo.query.get_or_404(repo_id)
    project = Project.query.filter_by(key=project_key).first()
    page = request.args.get('page', 1, type=int)

    issue_records = Issue.query.filter_by(
        repo_id=repo.github_repo_id, jira_project_key=project_key
    )
    pagination = issue_records.order_by(Issue.timestamp.asc()).paginate(
        page, per_page=10, error_out=False
    )
    issues = pagination.items

    return render_template(
        'issues.html',
        repo=repo,
        project=project,
        issues=issues,
        jira_base_url=ConfigValue.get_or_insert_jira_address(),
        pagination=pagination
    )
