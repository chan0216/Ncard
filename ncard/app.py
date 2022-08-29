from datetime import datetime
from flask import *
from flask_socketio import SocketIO, join_room, emit
import controller
import model.main

app = Flask(__name__)
app.register_blueprint(controller.api.user_blueprint, url_prefix='/api')
app.register_blueprint(controller.api.post_blueprint, url_prefix='/api')
app.register_blueprint(controller.api.verify_blueprint, url_prefix='/api')
app.register_blueprint(controller.api.ncard_blueprint, url_prefix='/api')
app.register_blueprint(controller.api.profile_blueprint, url_prefix='/api')
app.register_blueprint(controller.api.friend_blueprint, url_prefix='/api')
app.register_blueprint(controller.api.chats_blueprint, url_prefix='/api')
app.register_blueprint(controller.api.comments_blueprint, url_prefix='/api')
app.register_blueprint(controller.pages)
socketio = SocketIO(app)


@socketio.on('join_room')
def on_join(room_id):
    join_room(room_id)


@socketio.on('send_message')
def handle_send_message(data):
    try:
        time = datetime.now()
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        resp = model.main.handle_send_message(data, now)
        if resp:
            data["time"] = time.strftime("%m-%d %H:%M")
            emit("receive_message", data, room=data["room"])
    except Exception as e:
        return {"error": True}, 500
