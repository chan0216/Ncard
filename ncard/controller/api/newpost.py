from flask import *
import re
from model.model import s3
import model.newpost
from functools import wraps
from decouple import config
import jwt


newpost_blueprint = Blueprint('newpost', __name__)


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


@newpost_blueprint.route("/image", methods=["POST"])
def post_image():
    file = request.files['file']
    filename = file.filename
    s3.Bucket("myawscloudfiles").put_object(
        Key=file.filename, Body=file)
    return {"imgurl": f"https://d33yfiwdj1z4d4.cloudfront.net/{filename}"}


@newpost_blueprint.route("/newpost", methods=["POST"])
@token_required
def add_newpost(current_user):
    try:

        data = request. json
        first_img = None
        imgs = re.search(
            r"(https://.(.*?)[-\w]+\.(jpg|gif|png|jpeg$))", data["postText"])
        if imgs:
            first_img = imgs.group()
        resp = model.newpost.add_newpost(
            current_user, data, first_img)
        return resp
    except Exception as e:
        return {"error": True}, 500


@newpost_blueprint.route("/newpost", methods=["GET"])
def get_newpost():
    try:
        resp = model.newpost.get_newpost()
        return resp
    except Exception as e:
        return {"error": True}, 500


@newpost_blueprint.route("/articles", methods=["GET"])
def get_hot_articles():
    try:
        resp = model.newpost.get_hot_articles()
        return resp
    except Exception as e:
        return {"error": True}, 500


@newpost_blueprint.route("/post/<id>", methods=["GET"])
def get_article(id):
    try:
        current_user = None
        token = request.cookies.get('token')
        if token:
            jwt_data = jwt.decode(token.encode('UTF-8'),
                                  config("secret_key"), algorithms=["HS256"])
            current_user = jwt_data["user_id"]
        resp = model.newpost.get_article(id, current_user)
        return resp
    except Exception as e:
        return {"error": True}, 500


@newpost_blueprint.route("/post/<int:post_id>/like", methods=["PATCH"])
def patch_like(post_id):
    token = request.cookies.get('token')
    if not token:
        res = make_response(
            jsonify({"error": True, "message": "未登入系統，拒絕存取"}), 403)
        return res
    try:
        jwt_data = jwt.decode(token.encode('UTF-8'),
                              config("secret_key"), algorithms=["HS256"])
        current_user = jwt_data["user_id"]
        resp = model.newpost.patch_post_like(post_id, current_user)
        return resp
    except Exception as e:
        return {"error": True}, 500


@newpost_blueprint.route("/comment", methods=["POST"])
@token_required
def add_comment(current_user):
    try:
        data = request. json
        resp = model.newpost.add_comment(data, current_user)
        return resp
    except Exception as e:
        return {"error": True}, 500


@newpost_blueprint.route("/comment/<id>", methods=["GET"])
def get_comment(id):
    try:
        resp = model.newpost.get_comment(id)
        return resp
    except Exception as e:
        return {"error": True}, 500
