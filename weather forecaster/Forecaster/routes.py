from Forecaster import forecaster, forecast, mail, hasher, database as db
from datetime import datetime
from flask import render_template, url_for, flash, redirect, request
from Forecaster.forms import LoginForm, RegisterForm, UpdateAccount, ResetRequestForm, ResetPasswordForm
from Forecaster.models import User
from flask_login import current_user, login_required, login_user, logout_user
from flask_mail import Message



@forecaster.route("/")
@forecaster.route("/home")
def home():
    return render_template("weather.html",  title="Weather Forecaster - Home", forecast=forecast,
                           Date=datetime.utcnow().date())



@forecaster.route("/login", methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and hasher.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash(f"{current_user.username} has been logged in.", "success")
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Invalid email or password", "danger")
    return render_template("login.html",  title="Weather Forecaster - Login", form=form)



@forecaster.route("/register", methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegisterForm()
    if form.validate_on_submit():
        secret_password = hasher.generate_password_hash(form.password.data).decode("utf-8")
        new_user = User(username=form.username.data,email=form.email.data,
                        password=secret_password)
        db.session.add(new_user)
        db.session.commit()
        flash(f"Account for {form.username.data} has been created.", "success")
        login_user(new_user)
        return redirect(url_for("home"))
    return render_template("register.html",  title="Weather Forecaster - Register", form=form)



@forecaster.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))



@forecaster.route("/account", methods=["GET","POST"])
@login_required
def account():
    form = UpdateAccount()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("account.html", title=f"Weather Forecaster - Account - {current_user.username}",
                           form=form)



def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='TheOfficialJogSpenson@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)



@forecaster.route("/reset_password", methods=['GET', 'POST'])
def reset_request():    
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = ResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password", "info")
        return redirect(url_for("login"))
    return render_template("reset_request.html", title="Weather Forecaster - Reset Password",
                           form=form)



@forecaster.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    user = User.validate_reset_token(token)
    if not user:
        flash("Your reset token has expired or is invalid", "warning")
        return redirect(url_for("reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password_hash = hasher.generate_password_hash(form.password.data)
        user.password = password_hash
        db.session.commit()
        flash("You password has been reset", "success")
        return redirect(url_for("login"))
    return render_template("reset_password.html", title="Weather Forecaster - Reset Password",
                           form=form) 



@forecaster.errorhandler(404)
def error_404(error):
    return render_template("errors/404.html",title="404 error"), 404


@forecaster.errorhandler(500)
def error_500(error):
    return render_template("errors/500.html",title="500 error"), 500