from arboretum.app import app as my_app
from arboretum.app import socketio

socketio.run(my_app)
