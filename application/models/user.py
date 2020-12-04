from .base import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from .game import *
from flask_login import UserMixin
from flask import current_app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=True, nullable=False)
    player1_id = db.relationship('Game', backref = 'player1', lazy = 'dynamic', foreign_keys = 'Game.player1_id')
    player2_id = db.relationship('Game', backref = 'player2', lazy = 'dynamic', foreign_keys = 'Game.player2_id')
