#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""manage.py

Command line helpers to help manage the application.
"""

import os

from app import create_app, db
from app.models import User, Repo
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

if os.path.exists('.env'):
    print('Importing environment from .env...')

    from dotenv import load_dotenv
    load_dotenv()

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Repo=Repo)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def deploy():
    """Migrate database to latest revision"""
    from flask.ext.migrate import upgrade
    upgrade()


if __name__ == '__main__':
    manager.run()
