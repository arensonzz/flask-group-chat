from flask_socketio import SocketIO
from app import create_app, socketio


app = create_app()

if __name__ == "__main__":
    socketio.run(app)
