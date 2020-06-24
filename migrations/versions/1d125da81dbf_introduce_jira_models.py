
#
# Unless explicitly stated otherwise all files in this repository are licensed
# under the Apache 2 License.
#
# This product includes software developed at Datadog
# (https://www.datadoghq.com/).
#
# Copyright 2018 Datadog, Inc.
#

"""introduce jira models:

Revision ID: 1d125da81dbf
Revises: bb8492da24f1
Create Date: 2020-02-25 09:11:44.104279
"""

from alembic import op
import sqlalchemy as sa


revision = '1d125da81dbf'
down_revision = 'bb8492da24f1'


def upgrade():
    sequence = sa.schema.Sequence('subscriptions_id_seq')
    op.execute(sa.schema.CreateSequence(sequence))
    op.add_column(
        'subscriptions',
        sa.Column(
            'id',
            sa.Integer(),
            nullable=False,
            server_default=sa.func.next_value(sequence),
            autoincrement=True
        )
    )
    op.drop_constraint('subscribed_lists_subscription_board_id_subscription_repo_id_fkey',
                       'subscribed_lists', type_='foreignkey')
    op.add_column('subscriptions', sa.Column(
        'project_key', sa.String(length=64), nullable=True))
    op.drop_constraint('subscriptions_pkey', 'subscriptions', 'primary')
    op.create_primary_key('subscriptions_pkey', 'subscriptions', ["id", "repo_id", ])
    op.alter_column('subscriptions', 'board_id',
                    existing_type=sa.VARCHAR(length=64),
                    nullable=True)
    op.create_unique_constraint('subscriptions_board_id_key', 'subscriptions', ['board_id', 'repo_id'])
    op.create_unique_constraint('subscriptions_project_key_key', 'subscriptions', ['project_key', 'repo_id'])

    op.create_foreign_key('subscribed_lists_subscription_board_id_subscription_repo_id_fkey', 'subscribed_lists', 'subscriptions', [
                          'subscription_board_id', 'subscription_repo_id'], ['board_id', 'repo_id'])
    op.create_table('jira_issue_types',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.Text(), nullable=True),
                    sa.Column('description', sa.Text(), nullable=True),
                    sa.Column('issue_type_id', sa.String(
                        length=64), nullable=True),
                    sa.Column('subtask', sa.Boolean(), nullable=True),
                    sa.Column('timestamp', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('issue_type_id'),
                    )
    op.create_index(op.f('ix_jira_issue_types_timestamp'),
                    'jira_issue_types', ['timestamp'], unique=False)
    op.create_table('jira_members',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(length=100), nullable=True),
                    sa.Column('name', sa.String(length=100), nullable=True),
                    sa.Column('jira_member_id', sa.String(
                        length=64), nullable=True),
                    sa.Column('timestamp', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('jira_member_id')
                    )
    op.create_index(op.f('ix_jira_members_timestamp'),
                    'jira_members', ['timestamp'], unique=False)
    op.create_table('projects',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.Text(), nullable=True),
                    sa.Column('key', sa.String(length=64), nullable=True),
                    sa.Column('description', sa.Text(), nullable=True),
                    sa.Column('timestamp', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('key'),
                    sa.UniqueConstraint('name'),
                    )
    op.create_index(op.f('ix_projects_timestamp'),
                    'projects', ['timestamp'], unique=False)
    op.create_table('jira_parent_issues',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('summary', sa.String(length=64), nullable=True),
                    sa.Column('jira_issue_key', sa.String(
                        length=64), nullable=True),
                    sa.Column('timestamp', sa.DateTime(), nullable=True),
                    sa.Column('project_key', sa.String(length=64), nullable=True),
                    sa.ForeignKeyConstraint(['project_key'], ['projects.key'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('jira_issue_key')
                    )
    op.create_index(op.f('ix_jira_parent_issues_timestamp'),
                    'jira_parent_issues', ['timestamp'], unique=False)
    op.create_table('project_issue_types_helper',
                    sa.Column('project_id', sa.Integer(), nullable=False),
                    sa.Column('issue_type_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['issue_type_id'], ['jira_issue_types.id'], ),
                    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
                    sa.PrimaryKeyConstraint('project_id', 'issue_type_id')
                    )
    op.create_table('project_jira_members_helper',
                    sa.Column('project_id', sa.Integer(), nullable=False),
                    sa.Column('jira_member_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['jira_member_id'], ['jira_members.id'], ),
                    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
                    sa.PrimaryKeyConstraint('project_id', 'jira_member_id')
                    )
    op.create_foreign_key('subscriptions_project_key_fkey', 'subscriptions', 'projects', [
                          'project_key'], ['key'])
    op.create_table('subscribed_jira_issues',
                    sa.Column('subscription_project_key',
                              sa.String(length=64), nullable=False),
                    sa.Column('subscription_repo_id',
                              sa.Integer(), nullable=False),
                    sa.Column('jira_issue_key', sa.String(
                        length=64), nullable=False),
                    sa.Column('jira_member_id', sa.String(
                        length=64), nullable=True),
                    sa.Column('issue_type_name', sa.String(
                        length=32), nullable=False),
                    sa.Column('timestamp', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['jira_issue_key'], ['jira_parent_issues.jira_issue_key'], ),
                    sa.ForeignKeyConstraint(['subscription_project_key', 'subscription_repo_id'], [
                        'subscriptions.project_key', 'subscriptions.repo_id'], ),
                    sa.PrimaryKeyConstraint(
                        'subscription_project_key', 'subscription_repo_id', 'jira_issue_key')
                    )
    op.create_index(op.f('ix_subscribed_jira_issues_timestamp'),
                    'subscribed_jira_issues', ['timestamp'], unique=False)
    op.create_table('subscribed_jira_projects',
                    sa.Column('subscription_project_key',
                              sa.String(length=64), nullable=False),
                    sa.Column('subscription_repo_id',
                              sa.Integer(), nullable=False),
                    sa.Column('jira_member_id', sa.String(
                        length=64), nullable=True),
                    sa.Column('issue_type_id', sa.String(64), nullable=True),
                    sa.Column('timestamp', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['subscription_project_key', 'subscription_repo_id'], [
                        'subscriptions.project_key', 'subscriptions.repo_id'], ),
                    sa.PrimaryKeyConstraint('subscription_project_key',
                                            'subscription_repo_id'),
                    sa.ForeignKeyConstraint(
                        ['issue_type_id'], ['jira_issue_types.issue_type_id'], )
                    )
    op.create_index(op.f('ix_subscribed_jira_projects_timestamp'),
                    'subscribed_jira_projects', ['timestamp'], unique=False)
    op.add_column('issues', sa.Column('jira_issue_key',
                                      sa.String(length=64), nullable=True))
    op.add_column('issues', sa.Column('jira_parent_issue_key',
                                      sa.String(length=64), nullable=True))
    op.add_column('issues', sa.Column('jira_project_key',
                                      sa.String(length=64), nullable=True))
    op.drop_constraint('uq_issues_list', 'issues', type_='unique')
    op.create_unique_constraint('uq_issues_list', 'issues', [
                                'trello_list_id', 'jira_project_key', 'jira_parent_issue_key', 'github_issue_id'])
    op.create_unique_constraint('issues_jira_issue_key_key', 'issues', ['jira_issue_key'])
    op.create_foreign_key('issues_jira_parent_issue_key_fkey', 'issues', 'jira_parent_issues', [
                          'jira_parent_issue_key'], ['jira_issue_key'])
    op.create_foreign_key('issues_jira_project_key_fkey', 'issues', 'projects', [
                          'jira_project_key'], ['key'])
    op.add_column('pull_requests', sa.Column(
        'jira_issue_key', sa.String(length=64), nullable=True))
    op.add_column('pull_requests', sa.Column(
        'jira_parent_issue_key', sa.String(length=64), nullable=True))
    op.add_column('pull_requests', sa.Column(
        'jira_project_key', sa.String(length=64), nullable=True))
    op.drop_constraint('uq_pull_requests_list',
                       'pull_requests', type_='unique')
    op.create_unique_constraint('uq_pull_requests_list', 'pull_requests', [
                                'trello_list_id', 'jira_project_key', 'jira_parent_issue_key', 'github_pull_request_id'])
    op.create_unique_constraint('pull_requests_jira_issue_key_key', 'pull_requests', ['jira_issue_key'])
    op.create_foreign_key('pull_requests_jira_parent_issue_key_fkey', 'pull_requests', 'jira_parent_issues', [
                          'jira_parent_issue_key'], ['jira_issue_key'])
    op.create_foreign_key('pull_requests_jira_project_key_fkey', 'pull_requests', 'projects', [
                          'jira_project_key'], ['key'])


def downgrade():
    op.drop_constraint('pull_requests_jira_project_key_fkey', 'pull_requests', type_='foreignkey')
    op.drop_constraint('pull_requests_jira_parent_issue_key_fkey', 'pull_requests', type_='foreignkey')
    op.drop_constraint('pull_requests_jira_issue_key_key', 'pull_requests', type_='unique')
    op.drop_constraint('uq_pull_requests_list',
                       'pull_requests', type_='unique')
    op.create_unique_constraint('uq_pull_requests_list', 'pull_requests', [
                                'trello_list_id', 'github_pull_request_id'])
    op.drop_column('pull_requests', 'jira_project_key')
    op.drop_column('pull_requests', 'jira_parent_issue_key')
    op.drop_column('pull_requests', 'jira_issue_key')
    op.drop_constraint('issues_jira_project_key_fkey', 'issues', type_='foreignkey')
    op.drop_constraint('issues_jira_parent_issue_key_fkey', 'issues', type_='foreignkey')
    op.drop_constraint('issues_jira_issue_key_key', 'issues', type_='unique')
    op.drop_constraint('uq_issues_list', 'issues', type_='unique')
    op.create_unique_constraint('uq_issues_list', 'issues', [
                                'trello_list_id', 'github_issue_id'])
    op.drop_column('issues', 'jira_project_key')
    op.drop_column('issues', 'jira_parent_issue_key')
    op.drop_column('issues', 'jira_issue_key')
    op.drop_index(op.f('ix_subscribed_jira_projects_timestamp'),
                  table_name='subscribed_jira_projects')
    op.drop_table('subscribed_jira_projects')
    op.drop_index(op.f('ix_subscribed_jira_issues_timestamp'),
                  table_name='subscribed_jira_issues')
    op.drop_table('subscribed_jira_issues')
    op.drop_constraint('subscriptions_project_key_fkey', 'subscriptions', type_='foreignkey')
    op.drop_table('project_jira_members_helper')
    op.drop_table('project_issue_types_helper')
    op.drop_index(op.f('ix_jira_parent_issues_timestamp'),
                  table_name='jira_parent_issues')
    op.drop_table('jira_parent_issues')
    op.drop_index(op.f('ix_projects_timestamp'), table_name='projects')
    op.drop_table('projects')
    op.drop_index(op.f('ix_jira_members_timestamp'), table_name='jira_members')
    op.drop_table('jira_members')
    op.drop_index(op.f('ix_jira_issue_types_timestamp'),
                  table_name='jira_issue_types')
    op.drop_table('jira_issue_types')
    op.drop_constraint('subscribed_lists_subscription_board_id_subscription_repo_id_fkey',
                       'subscribed_lists', type_='foreignkey')
    op.drop_constraint('subscriptions_project_key_key', 'subscriptions', type_='unique')
    op.drop_constraint('subscriptions_board_id_key', 'subscriptions', type_='unique')
    op.alter_column('subscriptions', 'board_id',
                    existing_type=sa.VARCHAR(length=64),
                    nullable=False)
    op.drop_constraint('subscriptions_pkey', 'subscriptions', 'primary')
    op.create_primary_key('subscriptions_pkey', 'subscriptions', ["board_id", "repo_id", ])
    op.drop_column('subscriptions', 'project_key')
    op.create_foreign_key('subscribed_lists_subscription_board_id_subscription_repo_id_fkey', 'subscribed_lists', 'subscriptions', [
                          'subscription_board_id', 'subscription_repo_id'], ['board_id', 'repo_id'])
    op.drop_column('subscriptions', 'id')
    op.execute(sa.schema.DropSequence(sa.Sequence("subscriptions_id_seq")))
