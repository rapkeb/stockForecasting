from flask import Flask
from urls import configure_routes
import os
from dotenv import load_dotenv
from flask_login import LoginManager
from views import user_from_dict, users_collection
from bson import ObjectId
from flask_socketio import SocketIO
from flask_session import Session

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_NAME'] = 'session_app1'
Session(app)

socketio = SocketIO(app, cors_allowed_origins="*")


load_dotenv()
configure_routes(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to the login view if not authenticated
login_manager.login_message = "צריכים להיות מחוברים כדי לגשת לדף זה"

@login_manager.user_loader
def load_user(user_id):
    user_data = users_collection.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return user_from_dict(user_data)
    return None


@socketio.on('connect')
def handle_connect():
    print('Client connected')

socketio.init_app(app)


if __name__ == '__main__':
    socketio.run(debug=True, port=5005)


