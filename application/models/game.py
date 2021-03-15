from .base import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from .user import *

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.String(10), unique=True, nullable=False)
    game_data = db.Column(db.JSON, default={})
