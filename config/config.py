#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY", "some-super-duper-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
        'sqlite:///' + os.path.join(BASEDIR, '..', 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
