"""
filename: generate_events.py
author: Angelina Li
date: 03/07/2018
desc: helper script to generate some events for test database
"""

import csv
import random
from datetime import datetime, timedelta
from pytz import utc # timezone

def get_string(n):
    return n if n >= 10 else "0" + str(n)

def generate_fake_dates(n):
    dates = []
    for i in xrange(n):
        year = 2018
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
    new_users = []
    for i in xrange(n):
        new_users.append(random.choice(users))
    return new_users

def get_datetime(date_text):
    return utc.localize(datetime.strptime(date_text, "%Y-%m-%d-%H-%M"))

def get_second_dates(first_dates):
    second_dates = []
    for date_string in first_dates:
        date = get_datetime(date_string)
        add = timedelta(minutes=random.choice(range(15,60*25,15)))
        new_date = date + add
        second_dates.append(new_date.strftime("%Y-%m-%d-%H-%M"))
    return second_dates

def get_descriptions(n):
    descs = []
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
        "dance",
        "beach",
        "pub night",
        "trivia",
        "cleaning"
    ]
    for i in xrange(n):
        descs.append(random.choice(desc))
    return descs

def make_csv(filename, n):
    start_dates = generate_fake_dates(n)
    end_dates = get_second_dates(start_dates)
    usernames = get_fake_usernames(n)
    descs = get_descriptions(n)
    with open(filename, "w") as fl:
        headings = ["username", "desc", "start_dt", "end_dt"]
        writer = csv.writer(fl)
        writer.writerow(headings)
        for i in range(n):
            data = [usernames[i], descs[i], start_dates[i], end_dates[i]]
            writer.writerow(data)
    print("Done!")

if __name__ == "__main__":
    make_csv("files/test_events.csv", 500)
