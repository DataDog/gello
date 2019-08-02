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

"""EnvironmentVariableService"""

from os import environ
from .. import db
from ..models import ConfigValue
from ..services import ConfigValueService


class EnvironmentVariableService(object):
    """Service helpers related to non-sensitive environment variables."""

    def __init__(self):
        """Instantiates a new `EnvironmentVariableService`."""
        self.config_value_service = ConfigValueService()

    def update_persisted_variables(self):
        """Updates environment variables.

        Updates persisted non-sensitive environment variables with current
        environment variable values.

        Returns:
            None
        """
        for key, value in self._environment_variables().items():
            self.config_value_service.create(key=key, value=value)

        db.session.commit()

    def export_persisted_variables(self):
        """Exports persisted non-sensitive environment variables.

        Returns:
            None
        """
        environment_variables = ConfigValue.query.all()
        for variable in environment_variables:
            environ[variable.key] = variable.value

    def _environment_variables(self):
        """KVPs of current non-sensitive environment variables.

        Returns:
            dict(str:str)
        """
        return {
            e: environ.get(e) for e in self._environment_variable_names()
            if environ.get(e) is not None
        }

    def _environment_variable_names(self):
        """Names for non-sensitive configuration environment variables.

        Returns:
            list(str)
        """
        return ['TRELLO_ORG_NAME', 'GITHUB_ORG_LOGIN']
