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

"""project_service.py

Service-helpers for creating and mutating JIRA project data.
"""

from . import APIService
from . import JIRAService, JIRAMemberService
from .. import db
from ..models import Project, JIRAParentIssue, JIRAIssueType, JIRAMember


class ProjectService(APIService):
    """API persistent storage service.

    A class with the single responsibility of creating/mutating Project data.
    """

    def __init__(self):
        """Initializes a new BoardService object."""
        self.jira_service = JIRAService()
        self.jira_member_service = JIRAMemberService()

    def fetch(self):
        """Creates/Updates and persists all projects and corresponding JIRA
        issues and issue types.

        For each of the projects fetched by the `JIRAService`, insert or update
        them, then fetch the corresponding JIRA issues and issue types
        and insert or update them.

        Returns:
            None
        """
        # TODO: eventually we should probably update to using the REST API more
        # directly and leverage the experimental status filter so we can exclude
        # archived projects from the initial request from Jira instead of filtering
        # manually here
        try:
            fetched_projects = self.jira_service.projects()
            persisted_projects = Project.query.all()

            live_projects = list(
                filter(lambda x: (hasattr(x, "archived") and not getattr(x, "archived")) or not hasattr(x, "archived"), fetched_projects)
            )

            self._update_or_delete_projects(live_projects, persisted_projects)
            self._create_projects(live_projects, persisted_projects)

            db.session.commit()
        except Exception as error:
            print(error)

        # TODO: figure out if we need to manually delete archived projects, too

    def _update_or_delete_projects(self, fetched_projects, persisted_projects):
        """Updates or deletes `Project` records in the database.

        Args:
            fetched_projects (list(jira.Project)): The list of projects fetched
                from the JIRA API.
            persisted_projects (list(Project)): The list of persisted projects
                fetched from the database.

        Returns:
            None
        """
        fetched_project_dict = {proj.key: proj for proj in fetched_projects}
        fetched_project_names = [proj.name for proj in fetched_projects]

        for record in (persisted_projects or []):
            if record.key in fetched_project_dict or record.name in fetched_project_names:
                # Find the JIRA project by unique string `key`
                jira_proj = fetched_project_dict[record.key]

                # fetched_user_ids = {user.accountId for user in
                #                     self.jira_service.get_project_members(
                #                         record.key)}
                # persisted_users = {user.jira_member_id: user for user in
                #                    record.allowed_members}

                # for user in fetched_user_ids:
                #     if user not in persisted_users:
                #         member = JIRAMember.query.filter_by(
                #                     jira_member_id=user
                #                  ).first()
                #         if member:
                #             record.allowed_members.append(member)
                #     else:
                #         persisted_users.pop(user)

                # for user_id, user_object in persisted_users.items():
                #     if user_id not in fetched_user_ids:
                #         record.allowed_members.remove(user_object)

                # Update the attributes
                record.name = jira_proj.name

                # some Jira projects have changed their IDs since being
                # added into Gira; we want to update the keys where necessary
                if (record.key != jira_proj.key):
                    record.key = jira_proj.key

                # jira_issues = self.jira_service.get_project_issues(jira_proj.key)
                # jira_issue_types = self.jira_service.get_issue_types(jira_proj.key)

                # # Update or delete the existing issues for a given project
                # self._update_or_delete_issues(jira_issues, jira_proj.key)
                # # Add the new issues to the database for a given project
                # self._create_issues(jira_issues, jira_proj.key)
                # # Update or delete the existing issue types for a given project
                # self._update_or_delete_issue_types(jira_issue_types, record)
                # # Add the new issue types to the database for a given project
                # self._create_issue_types(jira_issue_types, record)

                db.session.add(record)
            else:
                # Then delete this project
                db.session.delete(record)

    def _create_projects(self, fetched_projects, persisted_projects):
        """Creates records that do not exist in the database.

        Args:
            fetched_projects (list(jira.Project)): The list of projects fetched
                from the JIRA API.
            persisted_projects (list(Project)): The list of persisted boards
                fetched from the database.

        Returns:
            None
        """
        persisted_project_ids = set(
            map(lambda x: x.key, persisted_projects)
        )

        projects_to_create = set(
            filter(lambda x: x.key not in persisted_project_ids, fetched_projects)
        )

        # TODO: make this async so we don't have to wait for each project's issues
        for jira_project in (projects_to_create or []):
            jira_project_model = Project(
                name=jira_project.name,
                key=jira_project.key,
            )

            # fetched_ids = [x.accountId for x in
            #                (self.jira_service.get_project_members(jira_project.key) or [])]

            # for jid in (fetched_ids or []):
            #     jira_member = JIRAMember.query.filter_by(jira_member_id=jid).first()
            #     if jira_member:
            #         jira_project_model.allowed_members.append(jira_member)

            db.session.add(jira_project_model)

            # Create all the associated parent issues and issue types for the newly created project
            # jira_issues = self.jira_service.get_project_issues(jira_project.key)
            # jira_issue_types = self.jira_service.get_issue_types(jira_project.key)
            # self._create_issues(jira_issues, jira_project.key)
            # self._create_issue_types(jira_issue_types, jira_project_model)

    def _update_or_delete_issues(self, fetched_issues, project_key):
        """Updates or deletes existing `JIRAParentIssue`s in the database.

        Args:
            fetched_issues (list(jira.Issue)): JIRA Issue objects to be
                updated if the `issue.key` matches the `jira_issue_key` for
                the existing `JIRAParentIssue` record, or deleted if not.
            project_key (str): The key of the `Project` the issues are associated to.

        Returns:
            None
        """
        fetched_issue_dict = {iss.key: iss for iss in fetched_issues}
        persisted_issues = JIRAParentIssue.query.filter_by(project_key=project_key)

        for record in (persisted_issues or []):
            if record.jira_issue_key in fetched_issue_dict:
                # Find the jira issue by unique string `jira_issue_key`
                jira_issue = fetched_issue_dict[record.jira_issue_key]

                # Update the attributes
                issue_summary = jira_issue.fields.summary if len(jira_issue.fields.summary) <= 64 else jira_issue.fields.summary[:61] + "..."  # Truncate issue due to table constraint
                record.summary = issue_summary
                record.jira_issue_key = jira_issue.key
            else:
                db.session.delete(record)

    def _create_issues(self, fetched_issues, project_key):
        """Inserts new `JIRAParentIssue`s into the database.

        Args:
            fetched_issues (list(JIRA.Issue)): JIRA Issue objects to be
                inserted into the database.
            project_key (str): The key of the `Project` the issues will be associated
                to.

        Returns:
            None
        """
        persisted_issues = JIRAParentIssue.query.filter_by(project_key=project_key)

        try:
            persisted_issue_keys = set(
                map(lambda x: x.jira_issue_key, (persisted_issues or []))
            )

            jira_issues_to_create = list(
                filter(
                    lambda x: x.key not in persisted_issue_keys,
                    (fetched_issues or [])
                )
            )
        except Exception as error:
            jira_issues_to_create = []
            print (error)

        for jira_issue in (jira_issues_to_create or []):
            issue_summary = jira_issue.fields.summary if len(jira_issue.fields.summary) <= 64 else jira_issue.fields.summary[:61] + "..."
            jira_issue_model = JIRAParentIssue(
                summary=issue_summary,
                jira_issue_key=jira_issue.key,
                project_key=project_key
            )
            db.session.add(jira_issue_model)

    def _update_or_delete_issue_types(self, fetched_issue_types, project):
        """Updates or deletes `JIRAIssueType`s from the database.

        Args:
            fetched_issues (list(JIRA.IssueType)): JIRA Issue Type objects to
                be inserted into the database.
            project_key (str): The key of the `Project` the issues types will
                be associated to.

        Returns:
            None
        """
        persisted_issue_types = project.issue_types
        fetched_type_dict = {issue_type.id: issue_type for issue_type in fetched_issue_types}

        for issue_type in (persisted_issue_types or []):
            if issue_type.issue_type_id in fetched_type_dict:
                fetched_issue_type = fetched_type_dict[issue_type.issue_type_id]
                issue_type.name = fetched_issue_type.name
                issue_type.subtask = fetched_issue_type.subtask
            else:
                project.issue_types.remove(issue_type)
                if not len(issue_type.projects):
                    db.session.delete(issue_type)

    def _create_issue_types(self, fetched_issue_types, project):
        """Inserts new `JIRAIssueType`s into the database.

        Args:
            fetched_issues (list(JIRA.IssueType)): JIRA Issue Type objects to
                be inserted into the database.
            project_key (str): The key of the `Project` the issues types will
                be associated to.

        Returns:
            None
        """
        try:
            persisted_issue_types = set(map(lambda x: x.issue_type_id,
                                            project.issue_types))

            issue_types_to_create = list(
                filter(
                    lambda x: x.id not in persisted_issue_types,
                    fetched_issue_types
                )
            )
        except Exception as error:
            issue_types_to_create = []
            print(error)

        for issue_type in (issue_types_to_create or []):
            persisted_issue_type = JIRAIssueType.query.filter_by(
                issue_type_id=issue_type.id
            ).first()
            if not persisted_issue_type:
                persisted_issue_type = JIRAIssueType(
                    name=issue_type.name,
                    description=None,
                    issue_type_id=issue_type.id,
                    subtask=issue_type.subtask
                )
                db.session.add(persisted_issue_type)

            project.issue_types.append(persisted_issue_type)
