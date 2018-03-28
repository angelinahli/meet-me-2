#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateTimeField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email

from app.models import User
from app.program_info import info

# helper classes

class DataReqMsg(DataRequired):
    def __init__(self):
        DataRequired.__init__(self, message="Data required")

# form classes

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataReqMsg()])
    password = PasswordField("Password", validators=[DataReqMsg()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")

class SignUpForm(FlaskForm):
    user_help_text = ("Username should be longer than 4 characters and can " + 
        "only include letters and numbers.")
    pass_help_text = ("Password should be longer than 6 characters and " + 
        "include at least 1 of each: lower case letter, upper case letter " + 
        "and number")

    first_name = StringField("First Name", validators=[DataReqMsg()])
    last_name = StringField("Last Name", validators=[DataReqMsg()])
    email = StringField("Email", validators=[DataReqMsg(), Email()])
    username = StringField("Username", validators=[DataReqMsg()])
    password = PasswordField("Password", validators=[DataReqMsg()])
    confirm = PasswordField("Repeat Password", validators=[
        EqualTo("password", message="Passwords must match.")
    ])
    submit = SubmitField("Create Account")

    def validate_username(self, username):
        length = len(username)
        if length < 4:
            raise ValidationError(
                "Username must be at least 4 characters long!")
        if length > 64:
            raise ValidationError(
                "Username must be less than 64 characters long!")
        if not username.isalphanum():
            raise ValidationError(
                "Username can only contain letters and numbers!")
        
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Sorry - this username is taken!")

    def validate_password(self, password):
        if len(password) < 6:
            raise ValidationError(
                "Password must be at least 6 characters long!")
        if not re.search("[a-z]", password):
            raise ValidationError("Password must contain a lower case letter!")
        if not re.search("[A-Z]", password):
            raise ValidationError("Password must contain a upper case letter!")
        if not re.search("[0-9]", password):
            raise ValidationError("Password must contain a number!")
        if re.search("\s", password):
            raise ValidationError(
                "Password cannot contain whitespace characters!")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(
                "There is already an account associated with this email")

class SettingsForm(FlaskForm):
    pass_help_text = ("Password should be longer than 6 characters and " + 
        "include at least 1 of each: lower case letter, upper case letter " + 
        "and number")

    first_name = StringField("First name", validators=[DataReqMsg()])
    last_name = StringField("Last name", validators=[DataReqMsg()])
    username = StringField("Username", validators=[DataReqMsg()])
    email = StringField("Email", validators=[DataReqMsg(), Email()])
    password = PasswordField("Password", validators=[DataReqMsg()])
    new_password = PasswordField("New Password", validators=[DataReqMsg()])
    confirm = PasswordField("Repeat", validators=[
        EqualTo("new_password", message="Passwords must match.")
    ])
    submit = SubmitField("Save")
    delete = SubmitField("Delete Account")

    def validate_new_password(self, new_password):
        if len(new_password) < 6:
            raise ValidationError(
                "Password must be at least 6 characters long!")
        if not re.search("[a-z]", new_password):
            raise ValidationError("Password must contain a lower case letter!")
        if not re.search("[A-Z]", new_password):
            raise ValidationError("Password must contain a upper case letter!")
        if not re.search("[0-9]", new_password):
            raise ValidationError("Password must contain a number!")
        if re.search("\s", new_password):
            raise ValidationError(
                "Password cannot contain whitespace characters!")


class NewEventForm(FlaskForm):
    event_name = StringField("Event name", validators=[DataReqMsg()])
    start_time = DateTimeField("Start period", validators=[
        DataRequired(message="Invalid datetime format.")
    ])
    end_time = DateTimeField("End period", validators=[
        DataRequired(message="Invalid datetime format.")
    ])
    minutes = IntegerField("Total time needed (minutes)", validators=[DataReqMsg()])
    usernames = StringField("Usernames", validators=[DataReqMsg()])
