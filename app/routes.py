from flask import render_template
from app import app
from forms import LoginForm, SignUpForm

from program_info import info

@app.route("/")
@app.route("/index/")
def index():
    return render_template("index.html", title="Meet Me")

@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    return render_template("login.html", title="Login", form=form)

@app.route("/register/", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    return render_template("sign_up.html", title="Sign Up", form=form, info=info)