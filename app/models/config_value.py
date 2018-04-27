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

from .. import db


class ConfigValue(db.Model):
    __tablename__ = 'config_values'

    # Attributes
    key = db.Column(db.Text(), unique=True, primary_key=True)
    value = db.Column(db.Text(), unique=False)
