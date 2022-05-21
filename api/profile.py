from flask import *
from decouple import config
import jwt
from functools import wraps
profile_blueprint = Blueprint('profile', __name__)


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


@profile_blueprint.route("/api/profile", methods=["POST"])
@token_required
def profile(current_user):
    data = request. json
    print(current_user)
    print(data)
    return {"ok": True}
