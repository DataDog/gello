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

"""onboarding/__init__.py

onboarding module initialization code.
"""

from flask import Blueprint

onboarding = Blueprint('onboarding', __name__)

from . import views
