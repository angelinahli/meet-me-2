from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateTimeField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

from program_info import info

# helper classes

class DataReqMsg(DataRequired):
    def __init__(self):
        DataRequired.__init__(self, message="Data required.")

class LengthMsg(Length):
    def __init__(self, len_dict, field_name):
        lmin = len_dict["min"]
        lmax = len_dict["max"]
        lmessage = ("Please provide a {name} between {min} and " + 
            "{max} characters long.").format(
                name=field_name,
                min=lmin,
                max=lmax
        )
        Length.__init__(self, min=lmin, max=lmax, message=lmessage)

# form classes

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataReqMsg()])
    password = PasswordField("Password", validators=[DataReqMsg()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")

class SignUpForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataReqMsg()])
    last_name = StringField("Last Name", validators=[DataReqMsg()])
    username = StringField("Username", validators=[
        DataReqMsg(),
        LengthMsg(info["username"], "username")
    ])
    password = PasswordField("Password", validators=[
        DataReqMsg(),
        LengthMsg(info["password"], "password"),
    ])
    confirm = PasswordField("Repeat Password", validators=[
        EqualTo("password", message="Passwords must match.")
    ])
    submit = SubmitField("Create Account")

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
