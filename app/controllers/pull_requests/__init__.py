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

"""__init__.py

pull_requests module initialization code.
"""

from flask import Blueprint

pull_request = Blueprint('pull_request', __name__)

from . import views
