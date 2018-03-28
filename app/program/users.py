"""
Module for functions related to user
"""
import os
import sys
import flask_login as fl
from flask import flash, request

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
    fl.login_user(user, remember=remember_me)

def update_user_settings(
        username, 
        email, 
        first_name, 
        last_name, 
        password, 
        new_password):
    user = fl.current_user
    if not user.check_password(password):
        raise FlaskException("This password is invalid!", "error")
    req = request.form["submit"]
    if req == "delete":
        # I'm not sure if this will delete events associated too
        db.session.delete(user)
        db.session.commit()
    elif req == "submit":
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        if new_password:
            user.password = new_password
        db.session.commit()