import os
from flask import Flask
from .accounts.views import accounts
from .main.views import main
from flask_restful import Resource, Api
from flask_socketio import SocketIO

socketio = SocketIO()

def create_app():
    app = Flask(__name__,template_folder="templates")
    api = Api(app)

    app.config["DEBUG"] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get(
    'SQLALCHEMY_TRACK_MODIFICATIONS')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
    app.config['USER_AUTO_LOGIN_AFTER_REGISTER'] = True
    app.config['USER_ENABLE_NOCONFIRM_LOGIN'] = True
    app.config['USER_CONFIRM_EMAIL'] = False
    app.config['USER_ENABLE_CONFIRM_EMAIL'] = False
    app.register_blueprint(accounts)
    app.register_blueprint(main)
    app.config['TEMPLATES_AUTO_RELOAD']=True

    return app
