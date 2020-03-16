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

"""jira_subscriptions/forms.py

JIRA Subscription-related forms.
"""


import re
import textwrap

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import Required, Length
from ...models import Project, JIRAIssueType, Repo, Subscription


class NewSubscriptionForm(FlaskForm):
    """Form for creating a new JIRA subscription."""
    project_name = StringField(
        'Project Name',
        validators=[Required(), Length(1, 63)],
        description=textwrap.dedent(
            """
            The name of the JIRA project you wish to add new issues to
            """
        )
    )
    repo_name = StringField(
        'Repo Name',
        validators=[Required(), Length(1, 100)],
        description=textwrap.dedent(
            """
            The name of a GitHub repository you wish to register event webhooks
            for
            """
        )
    )
    issue_type = StringField(
        'Issue Type Name',
        description=textwrap.dedent(
            """
            The name of the Issue type that you would like to assign to all JIRA
            issues made by this subscription (Note: only applies to JIRA issues
            without a parent issue). If no issue type is provided, the issue type
            is assumed to be "Task"
            """
        )
    )
    parent_issues = StringField(
        'JIRA Issue keys',
        description=textwrap.dedent(
            """
            A comma delimited list of <code>JIRAParentIssues.jira_issue_key</code>s
            belonging to the <code>Project</code> associated with the
            <code>project_key</code> above. An empty list article will result
            in the JIRA issues being created without a parent issue. Duplicates
            will be ignored.
            """
        )
    )
    issue_autocard = BooleanField(
        'Issue Autocard',
        description=textwrap.dedent(
            """
            If checked, JIRA issues will automatically be created when a
            contributor outside of your organization submits a
            <a href='https://help.github.com/articles/about-issues/'>GitHub
            Issue</a>.
            """
        )
    )
    pull_request_autocard = BooleanField(
        'Pull Request Autocard',
        description=textwrap.dedent(
            """
            If checked, JIRA issues will automatically be created when a
            contributor outside of your organization submits a
            <a href='https://help.github.com/articles/about-pull-requests/'>
            Pull Request</a>.
            """
        )
    )
    submit = SubmitField('Create')

    def validate(self):
        """Performs validations of the form field values.

        - Validates the `project_name` attribute belongs to a `Project`
        - Validates the `repo_name` attribute belongs to a `Repo`
        - Validates the `jira_issue_key` attribute is a comma-delimited list of
          `JIRAParentIssue.jira_issue_key` belonging to the `Project` with
          `project_key`.
        """
        project_name = self.project_name.data.strip()
        repo_name = self.repo_name.data.strip()
        issue_type_name = self.issue_type.data.strip()
        keys = self.parent_issues.data.strip()

        if not issue_type_name:
            issue_type_name = 'Task'

        # Perform project-specific validations
        project = Project.query.filter_by(name=project_name).first()
        if project is None:
            self._error_message = textwrap.dedent(
                f"""
                Project '{project_name}' does not exist
                """
            )
            return False

        # Get the `board_id` to return back to `views.py`
        self._project_key = project.key

        # Perform repo-specific validations
        repo = Repo.query.filter_by(name=repo_name).first()
        if repo is None:
            self._error_message = textwrap.dedent(
                f"""
                Repo '{repo_name}' does not exist
                """
            )
            return False

        # Get the `repo_id` to return back to `views.py`
        self._repo_id = repo.github_repo_id

        # Validate the `Subscription` does not already exist
        subscription = Subscription.query.filter_by(project_key=self._project_key,
                                                    repo_id=self._repo_id
                                                    ).first()
        if subscription is not None:
            self._error_message = textwrap.dedent(
                f"""
                Subscription exists for {project_name} and {repo_name}
                """
            )
            return False

        keys_set = set(re.split("\s*,\s*", keys))

        # Validate that all parent issue ids passed in are either blank or a
        # valid JIRAParentIssue associated to the 'project_key'

        valid_keys_set = True
        for issue_key in keys_set:
            if not issue_key or bool(project.parent_issues.filter_by(jira_issue_key=issue_key).first()):
                continue
            valid_keys_set = False
            break

        if not valid_keys_set:
            self._error_message = textwrap.dedent(
                f"""
                The `keys_list` passed in contains invalid entries
                """
            )
            return False

        self._keys_list = list(keys_set)

        # Perform issue type-specific validations
        issue_type = None
    
        if not bool(issue_type_name):
            if '' not in keys_set:
                self._error_message = textwrap.dedent(
                    f"""
                    A JIRA issue type is required for a subscriptions creating non-subtask JIRA issues
                    """
                )
                return False
        else:
            for jira_issue_type in JIRAIssueType.query.filter_by(name=issue_type_name):
                if any(x.issue_type_id == jira_issue_type.issue_type_id
                       for x in project.issue_types):
                    issue_type = jira_issue_type
                    break
            if not issue_type:
                self._error_message = textwrap.dedent(
                    f"""
                    Issue type {issue_type_name} does not exist for project {project_name}
                    """
                )
                return False

            if issue_type.subtask:
                self._error_message = textwrap.dedent(
                    f"""
                    Issue type {issue_type_name} for project {project_name} is a subtask issue type
                    """
                )
                return False

        self._issue_type = issue_type

        # All custom validations passed
        return True

    def get_project_key(self):
        return self._project_key

    def get_repo_id(self):
        return self._repo_id

    def get_issue_type(self):
        return self._issue_type

    def get_issue_keys(self):
        return self._keys_list

    def get_error_message(self):
        return self._error_message


class UpdateForm(FlaskForm):
    """Form for updating an existing subscription."""
    issue_autocard = BooleanField('Issue Autocard')
    pull_request_autocard = BooleanField('Pull Request Autocard')
    submit = SubmitField('Update')


class DeleteForm(FlaskForm):
    """Form for deleting an existing subscription."""
    submit = SubmitField('Delete')
