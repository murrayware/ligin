import os
from flask_seeder import FlaskSeeder
from .app import create_app, socketio
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_migrate import Migrate
from .accounts.views import accounts
from .main.views import main
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect
from .models import base
from .models.user import User
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_cors import CORS

# from flask_login_multi.login_manager import LoginManager


load_dotenv()
app=create_app()
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'accounts.login'
login_manager.login_message_category = 'info'
mail = Mail(app)
mail.init_app(app)
migrate = Migrate(app, base.db)
seeder = FlaskSeeder()
seeder.init_app(app, base.db)
CSRFProtect(app)
socketio.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
