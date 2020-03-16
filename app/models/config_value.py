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

"""config_value.py

ConfigValue model.
"""

from os import environ

from .. import db


class ConfigValue(db.Model):
    __tablename__ = 'config_values'

    # Attributes
    key = db.Column(db.Text(), unique=True, primary_key=True)
    value = db.Column(db.Text(), unique=False)

    def get_or_insert_jira_address():
        to_return = db.session.query(ConfigValue).get('JIRA_SERVER_ADDRESS')
        if bool(to_return):
            return to_return.value
        else:
            server = environ.get('JIRA_SERVER_ADDRESS')
            if not server:
                return ''
            if server[-1] == '/':
                server = server[:-1]
            cv = ConfigValue(key='JIRA_SERVER_ADDRESS', value=server)
            db.session.add(cv)
            db.session.commit()
            return server
