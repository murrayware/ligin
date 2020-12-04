from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import Form, StringField, PasswordField, BooleanField, IntegerField ,SelectField, FieldList, FormField, HiddenField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from .models import *
from flask_login import current_user

##################################################################
# Everything here is related to a simple user
##################################################################
class RegistrationForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Length(min=4,max=30)])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])


    def validate_email(self,email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is taken, please choose another one ')

#This the form for login a user
class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Length(min=4,max=30)])
    password = PasswordField('Password',validators=[DataRequired()])

#This is the form for the reset password page

class RequestResetForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Length(min=4,max=30)] )

    def validate_email(self,email):
        email = User.query.filter_by(email=email.data).first()
        if email is None:
            raise ValidationError('There is no account with that email. You need to register ')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])

class UpdateAccountForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Length(min=4,max=30)])
    current_password = PasswordField('Current Password',validators=[DataRequired()])
    new_password = PasswordField('New Password',
                            validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                            validators=[DataRequired(),EqualTo('new_password')])

    def validate_email(self,email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('That email is taken, please choose another one ')

