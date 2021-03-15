from application import create_app, socketio
from flask_login import LoginManager
from application.models import *
from flask_jsglue import JSGlue

app=create_app(debug=True)
jsglue = JSGlue(app)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'accounts.login'
login_manager.login_message_category = 'info'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    socketio.run(app,port=5000,host= '0.0.0.0')
