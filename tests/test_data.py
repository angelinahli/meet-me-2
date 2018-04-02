"""
filename: test_data.py
author: Angelina Li
date: 03/28/2018
desc: create a script to load in and out test data
"""

import csv
import os
import sys
from datetime import datetime
from pytz import utc # timezone

sys.path.append(os.path.abspath(".."))
# print(sys.path)

from app import db
from app.models import User, Event

BASEDIR = os.path.abspath(os.path.dirname(__file__))
USERS = os.path.join(BASEDIR, "files", "test_users.csv")
EVENTS = os.path.join(BASEDIR, "files", "test_events.csv")
DTFORMAT = "%Y-%m-%d-%H-%M"

def get_data_from_csv(filepath):
    with open(filepath) as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        headings = next(reader)
        return [ dict(zip(headings, data)) for data in reader ]

def get_datetime(date_text):
    return utc.localize(datetime.strptime(date_text, DTFORMAT))    

def add_users():
    users = get_data_from_csv(USERS)
    for user_dict in users:
        password = user_dict.pop("password") # everyone should have a pssword
        u = User(**user_dict) # remaining data sufficient to create user
        u.set_password(password)
        db.session.add(u)
    db.session.commit()

def add_events():
    events = get_data_from_csv(EVENTS)
    for event_dict in events:
        username = event_dict.pop("username")
        event_dict["start_dt"] = get_datetime(event_dict["start_dt"])
        event_dict["end_dt"] = get_datetime(event_dict["end_dt"])
        e = Event(**event_dict)
        e.set_user_id(username)
        db.session.add(e)
    db.session.commit()

def insert_test_data():
    add_users()
    add_events()

def delete_test_data():
    for u in User.query.all():
        db.session.delete(u)
    for e in Event.query.all():
        db.session.delete(e)
    db.session.commit()

def view_db_data():
    users = User.query.all()
    for u in users:
        events = Event.query.filter_by(user_id=u.id).limit(5).all()
        print(u)
        for e in events:
            print "\t", e

if __name__ == "__main__":
    delete_test_data()
    insert_test_data()
    # view_db_data()
