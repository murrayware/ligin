from .base import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from .game import *
from flask_login import UserMixin
from flask import current_app





class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=True, nullable=False)
def get_user(ident):
  return User.query.get(int(ident))
