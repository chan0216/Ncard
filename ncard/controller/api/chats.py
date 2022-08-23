from flask import *
import jwt
from decouple import config
import controller.decorator as dec
import model.chats
chats_blueprint = Blueprint("chats", __name__)


@chats_blueprint.route('/message', methods=['GET'])
@dec.token_required
def get_room(current_user):
    try:
        resp = model.chats.get_room(current_user)
        return resp
    except Exception as error:
        return {'error': str(error)}, 500


@chats_blueprint.route('/messages', methods=['GET'])
@dec.token_required
def get_friends(current_user):
    try:
        resp = model.chats.get_friends(current_user)
        return resp
    except Exception as error:
        return {'error': str(error)}, 500


@chats_blueprint.route('/message/<int:id>', methods=['GET'])
def get_chats(id):
    try:
        page = int(request.args.get('page'))
        next_page = page + 1
        token = request.cookies.get('token')
        if token:
            jwtdata = jwt.decode(token.encode('UTF-8'),
                                 config("secret_key"), algorithms=["HS256"])
            current_user = jwtdata["user_id"]
        resp = model.chats.get_chats(page, next_page, id, current_user)
        return resp
    except Exception as error:
        return {'error': str(error)}, 500
