"""
Module for functions related to managing user sessions
"""
import os
import sys
from flask_login import login_user
sys.path.append(os.path.abspath(".."))

from app.models import User
from exceptions import FlashException

def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user == None:
        raise FlashException("This user doesn't exist!", "error")
    elif not user.check_password(password):
        raise FlashException("This password is invalid!", "error")
    else:
        login_user(user, remember=form.remember_me.data)