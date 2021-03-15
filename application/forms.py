from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import Form, StringField, PasswordField, BooleanField, IntegerField,SelectField, FieldList, FormField, HiddenField, DateField, FloatField, validators
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_login import current_user
from .models import *


class RegistrationForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Length(min=4,max=30)])
    username = StringField("Username", validators=[validators.Length(min=3, max=25), validators.DataRequired(message="Please Fill This Field")])

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
