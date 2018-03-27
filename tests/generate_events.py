"""
filename: generate_events.py
author: Angelina Li
date: 03/07/2018
desc: helper script to generate some events for test database
"""

import random
from datetime import datetime, timedelta
from pytz import utc # timezone

def get_string(n):
    return n if n >= 10 else "0" + str(n)

def generate_fake_dates(n):
    dates = []
    for i in xrange(n):
        year = random.choice(range(2017,2019))
        month = random.choice(range(1,13))
        day = random.choice(range(1,29))
        hour = random.choice(range(0,24))
        minutes = random.choice([0,10,15,20,30,40,45,50])
        datetime = "{year}-{month}-{day}-{hour}-{min}".format(
            year=get_string(year),
            month=get_string(month),
            day=get_string(day),
            hour=get_string(hour),
            min=get_string(minutes)
        )
        print datetime
        dates.append(datetime)
    return dates

def get_fake_usernames(n):
    users = ["angelinali", 
        "bjones",
        "harryjamespotter",
        "hfinn",
        "atticusisgreat",
        "denzel",
        "l1zz13b3nn3t",
        "sherlockholmes",
        "jwatson",
        "vdavis",
        "jackiechan",
        "devpatel123",
        "chiwetel",
        "lunadiego"
    ]
    for i in xrange(n):
        print random.choice(users)

def get_datetime(date_text):
    return utc.localize(datetime.strptime(date_text, "%Y-%m-%d-%H-%M"))

def get_second_dates(first_dates):
    for date_string in first_dates:
        date = get_datetime(date_string)
        add = timedelta(minutes=random.choice(range(15,60*25,15)))
        new_date = date + add
        print new_date.strftime("%Y-%m-%d-%H-%M")

def get_descriptions(n):
    desc = [
        "meal",
        "interview",
        "gym",
        "lecture",
        "study",
        "duelling",
        "coding",
        "work",
        "meeting",
        "laundry",
        "nap",
        "running",
        "cycling",
        "date",
        "walking",
        "watching a movie",
        "coffee break",
        "hang out with friends",
        "budgeting",
        "taxes",
        "kayaking",
        "baton twirling",
        "knitting",
        "dance"
    ]
    for i in xrange(n):
        print random.choice(desc)

print "\nFIRST DATES\n"
dates = generate_fake_dates(200)
print "\nSECOND DATES\n"
get_second_dates(dates)
print "\nUSERS\n"
get_fake_usernames(200)
print "\nDESCS\n"
get_descriptions(200)
