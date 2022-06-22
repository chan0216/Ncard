from flask import *
from functools import wraps
import jwt
from model.db import con_pool
import model.main
from decouple import config
pages = Blueprint("pages", __name__)


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


@pages.route("/")
def index():
    return render_template("index.html")


@pages .route("/login")
def signin():
    return render_template("login.html")


@pages.route("/verify/school")
def verify_school():
    return render_template("verify.html")


@pages.route("/new-post")
def newpost():
    return render_template("newpost.html")


@pages.route("/member")
def member():
    return render_template("member.html")


@pages.route("/my/profile")
def myprofile():
    return render_template("cardprofile.html")


@pages.route("/ncard")
def ncard():
    return render_template("ncard.html")


@pages.route("/my/friends")
def friends():
    return render_template("friends.html")


@pages.route("/post/<id>")
def attraction(id):
    return render_template("post.html")


@pages.route("/friend/<id>")
def get_friend_data(id):
    return render_template("mate.html")


@pages.route('/chats', methods=['GET'])
@token_required
def redirect_msg(current_user):
    # try:
    resp = model.main.redirect_msg(current_user)
    if resp:
        ncardid = resp[0]
        return redirect(url_for('pages.chats', id=ncardid))
    return redirect(url_for('pages.chats'))


@pages.route("/chats/<id>")
@pages.route("/chats/", defaults={'id': None})
def chats(id):
    if id:
        return render_template("chats.html")
    else:
        return render_template("nochats.html")
