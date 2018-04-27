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

"""ConfigValueService"""

from os import environ

from . import CRUDService
from .. import db
from ..models import ConfigValue


class ConfigValueService(CRUDService):
    """CRUD persistent storage service.

    A class with the single responsibility of creating/mutating ConfigValue
    data.
    """

    def create(self, key, value):
        """Creates and persists a new config_value record to the database.

        Args:
            key (str): The key to lookup.
            value (str): The value.

        Returns:
            None
        """
        config_value = ConfigValue.query.filter_by(key=key).first()

        if config_value is None:
            environ[key] = value
            config_value = ConfigValue(key=key, value=value)
            db.session.add(config_value)
            db.session.commit()
        else:
            self.update(key=key, value=value)

    def update(self, key, value):
        """Updates a persisted config_value.

        Args:

        Returns:
            None
        """
        environ[key] = value
        config_value = ConfigValue.query.filter_by(key=key).first()
        config_value.value = value
        db.session.commit()

    def delete(self, key):
        """Deletes an old, persisted config_value.

        Args:

        Returns:
            None
        """
        ConfigValue.query.filter_by(key=key).delete()
        db.session.commit()
