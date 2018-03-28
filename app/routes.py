#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required

from app import app, db
from app.forms import LoginForm, SignUpForm
from app.models import User, Event

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
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user == None:
            msg = "This user doesn't exist!"
            form.username.errors.append(msg)
        elif not user.check_password(password):
            msg = "This password is invalid!"
            form.password.errors.append(mg)
        else:
            login_user(user, remember=form.remember_me.data)
            flash("Hi {}!".format(user.first_name), "info")
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
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Welcome to the family, {}!!".format(
            user.first_name), "info")
        return redirect(url_for("login"))
    return render_template("sign_up.html", **dct)

@app.route("/logout/")
def logout():
    logout_user()
    flash("See you {}!".format(current_user.first_name))
    return redirect(url_for("index"))

@app.route("/settings/")
@login_required
def settings():
    dct = {"title": current_user.first_name + "'s Settings"}
    return render_template("settings.html", **dct)
