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

"""run.py

Run the application locally by runnnig:

    `python run.py`
"""

from app import app

if __name__ == '__main__':
    app.run(host="0.0.0.0")
