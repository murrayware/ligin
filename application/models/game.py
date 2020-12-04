from .base import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from .user import *

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    player2_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    game_id = db.Column(db.String(10), unique=True, nullable=False)
    game_data = db.Column(db.JSON, default={})
