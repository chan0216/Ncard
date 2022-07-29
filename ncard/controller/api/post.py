from flask import *
import re
from model.model import s3
import model.post
from decouple import config
import controller.decorator as dec
import jwt


post_blueprint = Blueprint('post', __name__)


@post_blueprint.route("/image", methods=["POST"])
def post_image():
    file = request.files['file']
    filename = file.filename
    s3.Bucket("myawscloudfiles").put_object(
        Key=file.filename, Body=file)
    return {"imgurl": f"https://d33yfiwdj1z4d4.cloudfront.net/{filename}"}


@post_blueprint.route("/post", methods=["POST"])
@dec.token_required
def add_new_post(current_user):
    try:

        data = request. json
        first_img = None
        imgs = re.search(
            r"(https://.(.*?)[-\w]+\.(jpg|gif|png|jpeg$))", data["postText"])
        if imgs:
            first_img = imgs.group()
        resp = model.post.add_new_post(
            current_user, data, first_img)
        return resp
    except Exception as e:
        return {"error": True}, 500


@post_blueprint.route("/posts", methods=["GET"])
def get_new_post():
    try:
        page = int(request.args.get('page'))
        resp = model.post.get_new_post(page)
        return resp
    except Exception as e:
        return {"error": True}, 500


@post_blueprint.route("/post/<id>", methods=["GET"])
def get_article(id):
    try:
        current_user = None
        token = request.cookies.get('token')
        if token:
            jwt_data = jwt.decode(token.encode('UTF-8'),
                                  config("secret_key"), algorithms=["HS256"])
            current_user = jwt_data["user_id"]
        resp = model.post.get_article(id, current_user)
        return resp
    except Exception as e:
        return {"error": True}, 500


@post_blueprint.route("/post/<int:post_id>/like", methods=["PATCH"])
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
        resp = model.post.patch_post_like(post_id, current_user)
        return resp
    except Exception as e:
        return {"error": True}, 500


@post_blueprint.route("/articles", methods=["GET"])
def get_hot_articles():
    try:
        resp = model.post.get_hot_articles()
        return resp
    except Exception as e:
        return {"error": True}, 500
