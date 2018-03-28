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

""""""

import os

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth
from ...models import User
from ... import db
from .forms import LoginForm


@auth.before_app_request
def before_request():
    """"""
    if current_user.is_authenticated:
        print('User authenticated.')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """"""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))

        flash('Invalid username or password.')

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    """"""
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/create', methods=['POST'])
def create_account():
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
    return 'Admin user created.'
