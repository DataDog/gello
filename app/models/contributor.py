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

"""contributor.py

Contributor model.
"""

from datetime import datetime
from .. import db


class Contributor(db.Model):
    __tablename__ = 'contributors'

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), unique=True)
    member_id = db.Column(db.Integer, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
