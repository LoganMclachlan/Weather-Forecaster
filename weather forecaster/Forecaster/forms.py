from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, Email, EqualTo, data_required, ValidationError
from Forecaster.models import User
from flask_login import current_user


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[Length(min=2,max=20),data_required()])
    email = StringField("Email", validators=[Email(),data_required()])
    password = PasswordField("Password", validators=[data_required()])
    confirm_password = PasswordField("Confirm Password", validators=[data_required(),EqualTo("password")])
    submit = SubmitField("Sign up")

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first() != None:
            raise ValidationError("That username is taken, please try a differant one.")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first() != None:
            raise ValidationError("That email is taken, please try a differant one.")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[Email(),data_required()])
    password = PasswordField("Password", validators=[data_required()])
    remember_me = BooleanField("Remeber Me")
    submit = SubmitField("Login")

class UpdateAccount(FlaskForm):
    username = StringField("Username", validators=[Length(min=2,max=20),data_required()])
    email = StringField("Email", validators=[Email(),data_required()])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            if User.query.filter_by(username=username.data).first() != None:
                raise ValidationError("That username is taken, please try a differant one.")

    def validate_email(self, email):
        if email.data != current_user.email:
            if User.query.filter_by(email=email.data).first() != None:
                raise ValidationError("That email is taken, please try a differant one.")


class ResetRequestForm(FlaskForm):
    email = StringField("Email", validators=[Email(),data_required()])
    submit = SubmitField("Send")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first() == None:
            raise ValidationError("No account with that email.")

class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[data_required()])
    confirm_password = PasswordField("Confirm Password", validators=[data_required(),EqualTo("password")])
    submit = SubmitField("Set Password")