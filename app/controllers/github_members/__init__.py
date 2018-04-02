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

"""github_members/__init__.py

github_member module initialization code.
"""

from flask import Blueprint

github_member = Blueprint('github_member', __name__)

from . import views
