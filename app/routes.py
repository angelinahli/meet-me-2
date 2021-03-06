#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from datetime import datetime, timedelta
from flask import render_template, redirect, request, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import or_, func

from app import app, db
from app.forms import LoginForm, SignUpForm, SettingsForm, NewEventForm
from app.models import User, Event
from app.program import Scheduler

@app.route("/")
@app.route("/index/")
def index():
    dct = {"title": "Meet Me"}
    return render_template("index.html", **dct)

@app.route("/login/", methods=["GET", "POST"])
def login():
    dct = {"title": "Login"}
    if current_user.is_authenticated:
        # if you're accidentally routed to the login page
        return redirect(url_for("index"))
    form = LoginForm()
    dct["form"] = form
    if form.validate_on_submit():
        user = form.user
        login_user(user, remember=form.remember_me)
        return redirect(url_for("index"))
    return render_template("login.html", **dct)

@app.route("/signup/", methods=["GET", "POST"])
def signup():
    dct = {"title": "Sign Up"}
    if current_user.is_authenticated:
        # if you're accidentally routed to the sign up page
        return redirect(url_for("index"))
    form = SignUpForm()
    dct["form"] = form
    if form.validate_on_submit():
        db.session.add(form.user)
        db.session.commit()
        flash("Welcome to the family, {}!!".format(form.user.first_name), 
            "info")
        return redirect(url_for("login"))
    return render_template("sign_up.html", **dct)

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/settings/", methods=["GET", "POST"])
@login_required
def settings():
    dct = {
        "title": "Settings",
        "current_user": current_user
    }
    form = SettingsForm()
    dct["form"] = form
    if form.validate_on_submit():
        if form.delete.data:
            username = current_user.username
            logout_user()
            u = User.query.filter_by(username=username).first()
            db.session.delete(u)
            db.session.commit()
            flash("Successfully deleted account!", "info")
            return redirect(url_for("index"))
        elif form.submit.data:
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.first_name = form.name.data.split()[0]
            current_user.full_name = form.name.data
            if form.new_password.data:
                current_user.set_password(form.new_password.data)
            db.session.commit()
            flash("Updated settings!", "info")
    return render_template("settings.html", **dct)

@app.route("/u/<username>/", methods=["GET", "POST"])
@app.route("/user/<username>/", methods=["GET", "POST"])
@login_required
def user(username):
    u = User.query.filter_by(username=username).first_or_404()
    dct = {"title": u.full_name.title(), "user": u}
    return render_template("user_page.html", **dct)

@login_required
@app.route("/new_event/", methods=["GET", "POST"])
def new_event():
    dct = {"title": "New Event"}
    form = NewEventForm()
    dct["form"] = form
    if form.validate_on_submit():
        events = form.sched.get_formatted_times()
        js_events = json.dumps(events)
        dct["events"] = js_events
        # dct["scheduler"] = form.sched
        dct["title"] = form.sched.name
        return render_template("new_event_times.html", **dct)
    return render_template("new_event.html", **dct)

@app.route("/test_new_event/", methods=["GET", "POST"])
def test_new_event():
    dct = {}
    sched = Scheduler(
        users=User.query.all(), 
        name="Test Event", 
        start_date=datetime.now().date(), 
        end_date=(datetime.now() + timedelta(days=20)).date(), 
        start_time=datetime.now().time(), 
        end_time=(datetime.now() + timedelta(minutes=200)).time(), 
        minutes=120
    )
    events = sched.get_formatted_times()
    js_events = json.dumps(events)
    dct["events"] = js_events
    dct["title"] = sched.name
    return render_template("new_event_times.html", **dct)

@login_required
@app.route("/search/", methods=["GET"])
def search():
    dct = {"title": "Search", "show_bar": True}
    query = request.args.get("search")
    if query:
        users = User.query.filter(or_(
            User.username.contains(query),
            User.first_name.contains(query), 
            User.full_name.contains(query),
            User.email == query)
        ).all()  # maybe a bad idea idk

        # redirect to user page if there is only one result
        if len(users) == 1:
            user = users[0]
            return redirect(url_for("user", username=user.username))
        dct["show_bar"] = False
        dct["title"] = "Search Results"
        dct["count"] = len(users)
        dct["users"] = users  # probably want to implement pages in the future
    return render_template("search_results.html", **dct)

