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

"""db_task.py

Abstract db base class for tasks.
"""

from celery.task import Task
from .. import db


class DBTask(Task):
    """An abstract base class for database-related tasks."""

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        db.session.rollback()
        super().on_failure(exc, task_id, args, kwargs, einfo)

    def run(self):
        """Implement in concretion."""
        raise NotImplementedError()
