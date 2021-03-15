import os
from pathlib import Path
import secrets
from flask import Blueprint,request,render_template,redirect,flash,url_for,current_app
from flask_login import login_user, current_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from dotenv import load_dotenv
from sqlalchemy import or_
import re
load_dotenv()
from ..forms import *
from . import accounts



bcrypt = Bcrypt()
mail = Mail()
app_root = Path(__file__).parents[1]



@accounts.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.online'))
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        form = RegistrationForm(
            email=email,
            username=username,
            password=password,
            confirm_password=confirm_password,
        )
        if form.validate_on_submit():

                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                user = User(
                    email=form.email.data,
                    username=form.username.data,
                    password=hashed_password,)

                db.session.add(user)
                db.session.commit()
                login_user(user)
                return redirect(url_for('main.online'))
    else:
        form = RegistrationForm(
            email="",
            username="",
            password="",
            confirm_password="",
        )
    return render_template('register.html', title='Register', form=form, )

@accounts.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.online'))
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        form = LoginForm(
            email=email,
            password=password
        )
        if form.validate_on_submit():
            user = User.query.filter_by(email=email).first()
            if user and bcrypt.check_password_hash(user.password, password):
                login_user(user)
                next_page = request.args.get('next')
                flash(f"Welcome {email}", 'success')
            else:
                flash(
                    f"Login Unsuccessful,Please check your email and Password!", 'danger')
                return redirect(url_for('accounts.login'))
    else:
        form = LoginForm(email="")
    return render_template('login.html', title='Login', form=form)

# route for the user to logout
@accounts.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('accounts.login'))

# route for the user to request a new password
@accounts.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.overview'))
    if request.method == 'POST':
        email = request.form["email"]
        form = RequestResetForm(email=email)
        if form.validate_on_submit():
            user = User.query.filter_by(email=email).first()
            send_reset_email(user)
            flash(
                'An email has been sent with instructions to reset your password', 'info')
            return redirect(url_for('accounts.login'))
    else:
        form = RequestResetForm(email='')
    return render_template('reset_request.html', title='Reset Password', form=form)

# route for the user to reset his password
@accounts.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.overview'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('accounts.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f"Thank You. Your Password has been updated.You can now log in", 'success')
        return redirect(url_for('accounts.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

# route for updating the user account
@accounts.route('/update_user', methods=['GET', 'POST'])
@login_required
def update_user():
    if request.method == 'POST':
        email = request.form["email"]
        current_password = request.form['current_password']
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]
        form = UpdateAccountForm(email=email,current_password=current_password,
                new_password=new_password,confirm_password=confirm_password)
        if form.validate_on_submit():
            if bcrypt.check_password_hash(current_user.password, current_password):
                hashed_password = bcrypt.generate_password_hash(
                    new_password).decode('utf-8')
                current_user.email = form.email.data
                current_user.password = hashed_password
                db.session.commit()
                flash(f"Thank You. Your Account has been updated.", 'success')
                return redirect(url_for('main.overview'))
    else:
        form = UpdateAccountForm(email=current_user.email, current_password="",
            new_password="",confirm_password="")
    return render_template("user_update.html",title='Update Account', form=form,last_updated=dir_last_updated())


# function to send email
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@ourserver.com',
                  recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link :
{url_for('accounts.reset_token',token=token,_external=True)}
    If you didn't make the request, please ignore this email
    '''
    mail.send(msg)


