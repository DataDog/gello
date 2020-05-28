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

"""subscribed_jira_items/forms.py

SubscribedJIRA Project/Issue-related forms.
"""

import textwrap

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from ...models import Project, JIRAIssueType, JIRAParentIssue, JIRAMember,\
                      SubscribedJIRAProject, SubscribedJIRAIssue


class NewForm(FlaskForm):
    """Form for creating a subscribed_jira_item."""
    issue_key = StringField(
        'Issue Key',
        description=textwrap.dedent(
            """
            The key of a JIRA issue associated with the subscribed JIRA project
            (leave empty for a non-subtask issue)
            """
        )
    )
    issue_type_name = StringField(
        'Issue Type',
        description=textwrap.dedent(
            """
            The name of the issue type for JIRA issues to be created under this
            subscribed item (defaults to `Sub-task` or `Subtask` if no JIRA issue is
            specified)
            """
        )
    )
    jira_id = StringField(
        'JIRA Member ID',
        description=textwrap.dedent(
            """
            An optional field to specify the JIRA ID for a member to be
            automatically assigned to any JIRA Issues created on this list
            """
        )
    )
    submit = SubmitField('Create')

    def __init__(self, project_key, repo_id):
        """Sets the `project_key` for the form."""
        FlaskForm.__init__(self)
        self._project_key = project_key
        self._repo_id = repo_id

    def validate(self):
        """Performs validations of the form field values.

        - Validates the `issue_key` attribute is a `JIRAParentIssue.jira_issue_key`
          belonging to the `Project` with `project_key`.
        - Validates the `jira_member_id `attribute belongs to a
          `JIRAMember`
        """
        issue_key = self.issue_key.data.strip()
        jira_id = self.jira_id.data.strip()
        issue_type_name = self.issue_type_name.data.strip()

        if issue_key:
            jira_issue = JIRAParentIssue.query.filter_by(
                jira_issue_key=issue_key, project_key=self._project_key
            ).first()

            if jira_issue is None:
                self._error_message = textwrap.dedent(
                    f"""
                    JIRA Issue '{issue_key}' does not exist for project '{self._project_key}'
                    """
                )
                return False

            # Validate the `SubscribedList` does not already exist
            if bool(SubscribedJIRAIssue.query.get(
                [self._project_key, self._repo_id, issue_key]
            )):
                self._error_message = textwrap.dedent(
                    f"""
                    Subscribed JIRA issue {issue_key} exists for {self._project_key}, {self._repo_id}
                    """
                )
                return False
        else:
            if bool(SubscribedJIRAProject.query.get(
                [self._project_key, self._repo_id]
            )):
                self._error_message = textwrap.dedent(
                    f"""
                    Subscribed JIRA project exists for {self._project_key}, {self._repo_id}
                    """
                )
                return False

        # Get the `issue_key` to return back to `views.py`
        self._issue_key = issue_key

        # `jira_issue_type` is optional only if no SubscribedJIRAProject exists for this subscription
        if not issue_key:
            if not issue_type_name:
                self._error_message = textwrap.dedent(
                    f"""
                    JIRA Issue Type required for non-subtask subscriptions
                    """
                )
                return False
            else:
                project = Project.query.filter_by(key=self._project_key).first()
                for jira_issue_type in JIRAIssueType.query.filter_by(name=issue_type_name):
                    if bool(project.issue_types.filter_by(
                        issue_type_id=jira_issue_type.issue_type_id)
                    ):
                        issue_type = jira_issue_type
                        break
                if not issue_type:
                    self._error_message = textwrap.dedent(
                        f"""
                        Issue type {issue_type_name} does not exist for project with key {project.key}
                        """
                    )
                    return False

                if issue_type.subtask:
                    self._error_message = textwrap.dedent(
                        f"""
                        Issue type {issue_type_name} for project with key {project.key} is a subtask issue type
                        """
                    )
                    return False
        else:
            issue_type = None

        self._issue_type = issue_type.issue_type_id if issue_type else None

        # `jira_member_id` is optional
        if not jira_id:
            self._jira_member_id = None
            return True

        jira_member = JIRAMember.query.filter_by(
            jira_member_id=jira_id
        ).first()

        if not bool(jira_member):
            self._error_message = textwrap.dedent(
                f"""
                JIRA Member '{jira_id}' does not exist
                """
            )
            return False

        # Get the `jira_member_id` to return back to `views.py`
        self._jira_member_id = jira_member.jira_member_id

        # All custom validations passed
        return True

    def get_issue_key(self):
        return self._issue_key

    def get_issue_type(self):
        return self._issue_type

    def get_jira_member_id(self):
        return self._jira_member_id

    def get_error_message(self):
        return self._error_message


class UpdateForm(FlaskForm):
    """Form for updating an existing subscribed jira item."""
    jira_update_id = StringField('JIRA Member ID')
    submit = SubmitField('Update')

    def validate(self):
        """Performs validations of the form field values.

        - Validates the `jira_member_id `attribute belongs to a
          `JIRAMember`
        """
        jira_id = self.jira_update_id.data.strip()

        # `jira_member_id` is optional
        if not jira_id:
            self._jira_member_id = None
            return True

        jira_member = JIRAMember.query.filter_by(
            jira_member_id=jira_id
        ).first()

        if not bool(jira_member):
            self._error_message = textwrap.dedent(
                f"""
                JIRA Member '{jira_id}' does not exist
                """
            )
            return False

        # Get the `jira_member_id` to return back to `views.py`
        self._jira_member_id = jira_member.jira_member_id

        # All custom validations passed
        return True

    def get_jira_member_id(self):
        return self._jira_member_id

    def get_error_message(self):
        return self._error_message


class DeleteForm(FlaskForm):
    """Form for deleting an existing subscribed_list."""
    submit = SubmitField('Delete')
