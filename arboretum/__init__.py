from flask import Flask
from flask_socketio import SocketIO

def create_app():
    # Flask config
    app = Flask(__name__)
    print("The name \n")
    print(__name__)
    print("The name end \n")
    app.secret_key = 'dev-secret'
    app.debug = True
    socketio = SocketIO(app)
    socketio.run(app)

