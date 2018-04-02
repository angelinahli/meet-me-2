#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from flask_login import UserMixin
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login

# classes

class User(db.Model, UserMixin):
    __tablename__ = "user"
    __table_args__ = {"mysql_engine": "InnoDB"}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    first_name = db.Column(db.String(64), index=True)
    full_name = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(256))
    events = db.relationship("Event", backref="user", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return "https://www.gravatar.com/avatar/{}?d=identicon&s={}".format(
            digest, size)
    
    def get_upcoming_events(self):
        events = []
        for e in self.events:
            if e.start_dt > datetime.now():
                events.append(e)
            if len(events) == 5:
                break
        return events

    def get_events_between_dts(self, start, end):
        events = []
        for e in self.events:
            if (e.start_dt > start and e.start_dt < end) or \
                    (e.end_dt > start and e.end_dt < end):
                events.append(e)
        return events

    def __repr__(self):
        return "<User #{id}: {username}>".format(
            id=self.id, 
            username=self.username
        )

class Event(db.Model):
    __tablename__ = "event"
    __table_args__ = {"mysql_engine": "InnoDB"}

    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(120), index=True)
    start_dt = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    end_dt = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), 
        onupdate="cascade")

    def set_user_id(self, username):
        u = User.query.filter_by(username=username).first()
        self.user_id = u.id

    def get_str_date(self):
        return self.start_dt.date().strftime("%A, %d %B %Y")

    def get_str_start(self):
        return self.start_dt.strftime("%I:%M%p")

    def get_str_end(self):
        diff_date = self.end_dt.date() != self.start_dt.date()
        if diff_date:
            return self.end_dt.strftime("%A, %d %B %I:%M%p")
        return self.end_dt.strftime("%I:%M%p")

    def __repr__(self):
        return "<Event #{id}: {desc}>".format(
            id=self.id,
            desc=self.desc,
        )

class Schedule(object):

    def __init__(self, user):
        """user: User object"""
        self.user = user
        self.events = self.user.events

# functions

@login.user_loader
def load_user(id):
    return User.query.get(int(id))