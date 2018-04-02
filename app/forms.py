#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import wtforms as wtf
import datetime as dt
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo, Email, Regexp, ValidationError

from app.models import User
from app.program import Scheduler

# helper functions

def check_username_exists(username):
    """ returns true if username exists """
    return User.query.filter_by(username=username).first() != None

def get_valid_username(email):
    userstub = email.split("@")[0]
    username = userstub
    i = 1
    while check_username_exists(username):
        username = userstub + str(i)
        i += 1
    return username

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
        if check_username_exists(un):
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

class CheckDateTime(object):

    def __init__(self, str_format, message):
        self.str_format = str_format
        self.message = message

    def __call__(self, form, field):
        str_dt = field.data
        try:
            new_dt = dt.datetime.strptime(str_dt, self.str_format)
        except ValueError:
            raise ValidationError(self.message)

# form classes

class LoginForm(FlaskForm):    
    email = wtf.StringField("Email", validators=[DataReqMsg(), Email()])
    password = wtf.PasswordField("Password", validators=[DataReqMsg()])
    remember_me = wtf.BooleanField("Remember Me")
    submit = wtf.SubmitField("Sign In")

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        fv = FlaskForm.validate(self)
        if not fv:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user == None:
            self.email.errors = list(self.email.errors)
            self.email.errors.append("Unknown email address")
            return False
        elif not user.check_password(self.password.data):
            self.password.errors = list(self.password.errors)
            self.password.errors.append("Invalid password")
            return False
        self.user = user
        return True

class SignUpForm(FlaskForm):
    name = wtf.StringField("First and Last Name", validators=[DataReqMsg()])
    email = wtf.StringField("Email", validators=[
        DataReqMsg(), 
        Email(),
        CheckEmail()])
    password = wtf.PasswordField("Password", validators=[
        DataReqMsg(), 
        CheckPassword()])
    submit = wtf.SubmitField("Create Account")

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        fv = FlaskForm.validate(self)
        if not fv:
            return False
        first_name = self.name.data.split()[0]
        em = self.email.data
        user = User(
            username=get_valid_username(em),
            email=em,
            first_name=first_name,
            full_name=self.name.data)
        user.set_password(self.password.data)
        self.user = user
        return True
    
class SettingsForm(FlaskForm):
    name = wtf.StringField("First and Last Name", validators=[DataReqMsg()])
    username = wtf.StringField("Username", validators=[
        DataReqMsg(),
        CheckUsername(changed_name=True)])
    email = wtf.StringField("Email", validators=[
        DataReqMsg(), 
        Email(),
        CheckEmail(changed_email=True)])
    password = wtf.PasswordField("Password", validators=[DataReqMsg()])
    new_password = wtf.PasswordField("New Password", validators=[
        CheckPassword(changed_password=True)])
    confirm = wtf.PasswordField("Repeat", validators=[
        EqualTo("new_password", message="Passwords must match.")])
    submit = wtf.SubmitField("Save")
    delete = wtf.SubmitField("Delete Account")

    def validate_password(self, password):
        pw = password.data
        if not current_user.check_password(pw):
            raise ValidationError("This password is invalid!")

class SearchForm(FlaskForm):
    query = wtf.StringField()
    submit = wtf.SubmitField()

class NewEventForm(FlaskForm):
    date_format = "%m/%d/%Y"
    time_format = "%I:%M %p"

    event_name = wtf.StringField("Name of your event", 
        validators=[DataReqMsg()])
    start_date = wtf.StringField("Earliest date of event",
        validators=[
            CheckDateTime(date_format, message="Invalid date format")
        ])
    end_date = wtf.StringField("Latest date of event",
        validators=[
            CheckDateTime(date_format, message="Invalid date format")
        ])
    start_time = wtf.StringField("Earliest start time of event",
        validators=[
            CheckDateTime(time_format, message="Invalid time format")
        ])
    end_time = wtf.StringField("Latest end time of event",
        validators=[
            CheckDateTime(time_format, message="Invalid time format")
        ])
    minutes = wtf.IntegerField("Time event will last (in minutes)", 
        validators=[DataReqMsg()])
    usernames = wtf.StringField("Usernames of attendees", 
        validators=[DataReqMsg()])
    submit = wtf.SubmitField("Plan Event")

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.sched = None

    def get_date(self, date_string):
        new_dt = dt.datetime.strptime(date_string, self.date_format)
        return new_dt.date()

    def get_time(self, time_string):
        new_dt = dt.datetime.strptime(time_string, self.time_format)
        return new_dt.time()

    def get_users(self, un_string):
        users = []
        for username in un_string.split(","):
            username = username.strip().lower()
            user = User.query.filter_by(username=username).first()
            if user == None:
                raise ValidationError("User {} doesn't exist!".format(username))
            users.append(user)
        return users

    def validate(self):
        fv = FlaskForm.validate(self)
        if not fv:
            return False

        try:
            users = self.get_users(self.usernames.data)
        except ValidationError as e:
            self.usernames.errors = list(self.usernames.errors)
            self.usernames.errors.append(str(e))
            return False

        self.sched = Scheduler(
            users=users,
            name=self.event_name.data,
            start_date=self.get_date(self.start_date.data),
            start_time=self.get_time(self.start_time.data),
            end_date=self.get_date(self.end_date.data),
            end_time=self.get_time(self.end_time.data),
            minutes=self.minutes.data)
        return True

