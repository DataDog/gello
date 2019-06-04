#!/usr/bin/env python
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

"""manage.py

Command line helpers to help manage the application.
"""

import os

from app import create_app, db
from app.models import User, Repo
from app.services import api_services
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

if os.path.exists('.env'):
    print('Importing environment from .env in manage.py...')

    from dotenv import load_dotenv
    load_dotenv()

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Repo=Repo)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def fetch():
    """Fetch data"""
    print("Fetching API data.")

    # Fetch the API Service data on deployment
    for api_service in api_services():
        api_service.fetch()

    print("Finished fetching API data.")


@manager.command
def deploy():
    """Creates the admin user if they do not exist."""
    import textwrap
    from app.models import User
    from app import db

    record = User.query.filter_by(
        email=os.environ.get('ADMIN_EMAIL')).first()

    if not os.environ.get('ADMIN_EMAIL') or \
       not os.environ.get('ADMIN_PASSWORD'):
        print(
            textwrap.dedent(
                f"""
                Please configure the `ADMIN_EMAIL` and `ADMIN_PASSWORD`
                environment variables in the Heroku app settings:
                https://dashboard.heroku.com/apps/your-app/settings.

                Then run `heroku run python manage.py deploy` to create your
                admin user account required to login to Gello.
                """
            )
        )
    elif not record:
        # Create admin user
        user = User(
            username='admin',
            name='Admin User',
            email=os.environ.get('ADMIN_EMAIL'),
            password=os.environ.get('ADMIN_PASSWORD')
        )

        # Add admin user to the database
        db.session.add(user)
        db.session.commit()

        print("Created admin user.")

    fetch()


if __name__ == '__main__':
    manager.run()
