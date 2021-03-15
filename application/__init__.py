import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail, Message
import os
from flask_seeder import FlaskSeeder
from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect
from .models import base
from .models.user import User
from flask_session import Session
import os


cors = CORS()

socketio=SocketIO(cors_allowed_origins="*", logger=True, engineio_logger=True)
class Config(object):
    SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

def create_app(debug=False):
    app = Flask(__name__,template_folder="templates")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get(
    'SQLALCHEMY_TRACK_MODIFICATIONS')
    # app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SECRET_KEY'] = 'the rivers not like niggas'
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
    app.config['USER_AUTO_LOGIN_AFTER_REGISTER'] = True
    app.config['USER_ENABLE_NOCONFIRM_LOGIN'] = True
    app.config['USER_CONFIRM_EMAIL'] = False
    app.config['USER_ENABLE_CONFIRM_EMAIL'] = False
    app.debug = debug
    app.config['SESSION_TYPE']='filesystem'
    from .accounts import accounts
    from .main import main
    app.register_blueprint(accounts)
    app.register_blueprint(main)
    CORS(app)
    db = SQLAlchemy(app)
    mail = Mail(app)
    mail.init_app(app)
    migrate = Migrate(app, base.db)
    seeder = FlaskSeeder()
    seeder.init_app(app, base.db)
    CSRFProtect(app)
    # socketio=SocketIO(app,cors_allowed_origins="*")
    # Session(app)
    socketio.init_app(app)
    return app
