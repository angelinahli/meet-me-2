"""
Module for functions related to user
"""
import os
import sys
import flask_login as fl
from flask import flash

sys.path.append(os.path.abspath(".."))

from app import db
from app.models import User
from exceptions import FlashException

def login_user(username, password, remember_me):
    user = User.query.filter_by(username=username).first()
    if user == None:
        raise FlashException("This user doesn't exist!", "error")
    elif not user.check_password(password):
        raise FlashException("This password is invalid!", "error")
    else:
        fl.login_user(user, remember=remember_me)

def register_user(username, email, first_name, last_name, password):
    user = User(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    flash("Welcome to the family, {}!!".format(user.first_name), "info")