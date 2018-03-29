#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateTimeField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError

from app.models import User
from app.program_info import info

# custom validators

class DataReqMsg(DataRequired):
    def __init__(self):
        DataRequired.__init__(self, message="Data required")

class CheckUsername(object):

    def __init__(self, changed_name=False):
        self.changed_name = changed_name

    def __call__(self, form, field): 
        un = field.data
        length = len(un)
        
        if self.changed_name and un == current_user.username:
            return
        if length < 4:
            raise ValidationError("Username must be at least 4 characters long!")
        if length > 64:
            raise ValidationError("Username must be less than 64 characters long!")
        if not un.isalnum():
            raise ValidationError("Username can only contain letters and numbers!")
        user = User.query.filter_by(username=un).first()
        if user is not None:
            raise ValidationError("Sorry - this username is taken!")

class CheckPassword(object):

    def __init__(self, changed_password=False):
        self.changed_password = changed_password

    def __call__(self, form, field):
        pw = field.data
        if self.changed_password and not pw:
            return
        if len(pw) < 6:
            raise ValidationError("Password must be at least 6 characters long!")
        if not re.search("[a-z]", pw):
            raise ValidationError("Password must contain a lower case letter!")
        if not re.search("[A-Z]", pw):
            raise ValidationError("Password must contain a upper case letter!")
        if not re.search("[0-9]", pw):
            raise ValidationError("Password must contain a number!")
        if re.search("\s", pw):
            raise ValidationError(
                "Password cannot contain whitespace characters!")

class CheckEmail(object):

    def __init__(self, changed_email=False):
        self.changed_email = changed_email

    def __call__(self, form, field):
        if self.changed_email and field.data == current_user.email:
            return
        user = User.query.filter_by(email=field.data).first()
        if user is not None:
            raise ValidationError(
                "There is already an account associated with this email")

# form classes

class LoginForm(FlaskForm):    
    username = StringField("Username", validators=[DataReqMsg()])
    password = PasswordField("Password", validators=[DataReqMsg()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        fv = FlaskForm.validate(self)
        if not fv:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user == None:
            self.username.errors = list(self.username.errors)
            self.username.errors.append("Unknown username")
            return False
        elif not user.check_password(self.password.data):
            self.password.errors = list(self.password.errors)
            self.password.errors.append("Invalid password")
            return False
        self.user = user
        return True

class SignUpForm(FlaskForm):
    user_help_text = ("Username should be longer than 4 characters and can " + 
        "only include letters and numbers.")
    pass_help_text = ("Password should be longer than 6 characters and " + 
        "include at least 1 of each: lower case letter, upper case letter " + 
        "and number")

    first_name = StringField("First Name", validators=[DataReqMsg()])
    last_name = StringField("Last Name", validators=[DataReqMsg()])
    email = StringField("Email", validators=[
        DataReqMsg(), 
        Email(),
        CheckEmail()])
    username = StringField("Username", validators=[
        DataReqMsg(), 
        CheckUsername()])
    password = PasswordField("Password", validators=[
        DataReqMsg(), 
        CheckPassword()])
    confirm = PasswordField("Repeat Password", validators=[
        EqualTo("password", message="Passwords must match.")])
    submit = SubmitField("Create Account")

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        fv = FlaskForm.validate(self)
        if not fv:
            return False
        user = User(
            username=self.username.data,
            email=self.email.data,
            first_name=self.first_name.data,
            last_name=self.last_name.data)
        user.set_password(self.password.data)
        self.user = user
    
class SettingsForm(FlaskForm):
    pass_help_text = ("Password should be longer than 6 characters and " + 
        "include at least 1 of each: lower case letter, upper case letter " + 
        "and number")

    first_name = StringField("First name", validators=[DataReqMsg()])
    last_name = StringField("Last name", validators=[DataReqMsg()])
    username = StringField("Username", validators=[
        DataReqMsg(),
        CheckUsername(changed_name=True)])
    email = StringField("Email", validators=[
        DataReqMsg(), 
        Email(),
        CheckEmail(changed_email=True)])
    password = PasswordField("Password", validators=[DataReqMsg()])
    new_password = PasswordField("New Password", validators=[
        CheckPassword(changed_password=True)])
    confirm = PasswordField("Repeat", validators=[
        EqualTo("new_password", message="Passwords must match.")])
    submit = SubmitField("Save")
    delete = SubmitField("Delete Account")

    def validate_password(self, password):
        pw = password.data
        if not current_user.check_password(pw):
            raise ValidationError("This password is invalid!")

class NewEventForm(FlaskForm):
    event_name = StringField("Event name", validators=[DataReqMsg()])
    start_time = DateTimeField("Start period", validators=[
        DataRequired(message="Invalid datetime format.")])
    end_time = DateTimeField("End period", validators=[
        DataRequired(message="Invalid datetime format.")])
    minutes = IntegerField("Total time needed (minutes)", validators=[DataReqMsg()])
    usernames = StringField("Usernames", validators=[DataReqMsg()])
