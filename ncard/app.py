from datetime import date, datetime, time, timedelta
from flask import *
from functools import wraps
import jwt
from flask_socketio import SocketIO, join_room, emit
import controller
from model.db import con_pool
from flask_mail import Mail, Message
from decouple import config


def token_required(f):
    @wraps(f)
    def decorated():
        token = request.cookies.get('token')
        if not token:
            res = make_response(
                jsonify({"error": True, "message": "未登入系統，拒絕存取"}), 403)
            return res
        try:
            jwtdata = jwt.decode(token.encode('UTF-8'),
                                 config("secret_key"), algorithms=["HS256"])
            current_user = jwtdata["user_id"]
        except Exception as e:
            res = make_response(
                jsonify({"error": True, "message": "伺服器內部錯誤"}), 500)
            return res
        return f(current_user)
    return decorated


# def create_app():
#     app = Flask(__name__)
#     app.config["JSON_AS_ASCII"] = False
#     app.config['JSON_SORT_KEYS'] = False
#     app.config["TEMPLATES_AUTO_RELOAD"] = True
#     app.config['MAIL_SERVER'] = 'smtp.gmail.com'
#     app.config['MAIL_PORT'] = 465
#     app.config['MAIL_USERNAME'] = config('MAIL_USERNAME')
#     app.config['MAIL_PASSWORD'] = config('MAIL_PASSWORD')
#     app.config['MAIL_USE_TLS'] = False
#     app.config['MAIL_USE_SSL'] = True
#     mail = Mail(app)
#     return app


# app = create_app()
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config['JSON_SORT_KEYS'] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.register_blueprint(controller.api.user_blueprint)
app.register_blueprint(controller.api.newpost_blueprint, url_prefix='/api')
app.register_blueprint(controller.api.verify_blueprint, url_prefix='/api')
app.register_blueprint(controller.api.ncard_blueprint)
app.register_blueprint(controller.api.cardprofile_blueprint, url_prefix='/api')
app.register_blueprint(controller.api.friend_blueprint, url_prefix='/api')
app.register_blueprint(controller.api.chats_blueprint, url_prefix='/api')
app.register_blueprint(controller.pages)
socketio = SocketIO(app, cors_allowed_origins='*')


@app.route('/chats', methods=['GET'])
@token_required
def redirect_msg(current_user):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(buffered=True)
        cursor.execute(
            "select `ncard_id` from message where user_id=%s ORDER BY id desc limit 1", (current_user,))
        last_ncardid = cursor.fetchone()
        if last_ncardid:
            ncardid = last_ncardid[0]
            return redirect(url_for('pages.chats', id=ncardid))
        return redirect(url_for('pages.chats'))
    finally:
        cursor.close()
        db.close()


@socketio.on('join_room')
def on_join(room_id):
    join_room(room_id)


@socketio.on('send_message')
def handle_send_message(data):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor()
        time = datetime.now()
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(
            "insert into message(ncard_id,user_id,message,time) VALUES (%s, %s, %s, %s)", (data["room"], data["userId"], data["message"], now))
        db.commit()
        data["time"] = time.strftime("%m-%d %H:%M")
        emit("receive_message", data, room=data["room"])
    finally:
        cursor.close()
        db.close()


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8000, debug=True)
