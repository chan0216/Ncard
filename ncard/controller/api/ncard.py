from flask import *
from datetime import date, datetime, time, timedelta
import controller.decorator as dec
import model.ncard


ncard_blueprint = Blueprint('ncard', __name__)


@ncard_blueprint.route("/ncard", methods=["GET"])
@dec.token_required
def get_ncard(current_user):
    try:
        today = date.today()
        yesterday = today - timedelta(days=1)
        resp = model.ncard.get_ncard(
            current_user, today, yesterday)
        return resp
    except:
        return {"error": True}, 500


@ncard_blueprint.route("/ncard", methods=["POST"])
@dec.token_required
def create_ncard(current_user):
    try:
        data = request. json
        message = data["message"]
        time = datetime.now()
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        today = date.today()
        yesterday = today - timedelta(days=1)
        resp = model.ncard.create_ncard(
            current_user, yesterday, now, message)
        return resp
    except:
        return {"error": True}, 500


@ncard_blueprint.route("/status", methods=["GET"])
@dec.token_required
def user_status(current_user):
    try:
        resp = model.ncard.user_status(current_user)
        return resp
    except:
        return {"error": True}, 500
