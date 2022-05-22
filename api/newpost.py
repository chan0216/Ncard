from flask import *
import re
from model.model import s3
from functools import wraps
from decouple import config
from model.db import con_pool
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


@newpost_blueprint.route("/api/image", methods=["POST"])
def postimage():
    file = request.files['file']
    filename = file.filename
    s3.Bucket("myawscloudfiles").put_object(
        Key=file.filename, Body=file)
    return {"imgurl": f"https://d33yfiwdj1z4d4.cloudfront.net/{filename}"}


@newpost_blueprint.route("/api/newpost", methods=["POST"])
@token_required
def newpost(current_user):
    # try:

    data = request. json
    print(data["postText"])
    first_img = None
    imgs = re.search(
        r"(https://.(.*?)[-\w]+\.(jpg|gif|png|jpeg$))", data["postText"])
    if imgs:
        first_img = imgs.group()
    db = con_pool.get_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("Insert Into newpost(userID ,title ,content ,time ,first_img) Values(%s, %s ,%s ,%s ,%s)",
                   (current_user, data["postTitle"], data["postText"], data["timenow"], first_img))
    db.commit()
    return {"ok": True}
    # except:
    #     db.rollback()
    #     return {"error": True},500
    # finally:
    #     db.close()


@newpost_blueprint.route("/api/newpost", methods=["GET"])
def getnewpost():
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT profile.gender,profile.school,newpost.title,newpost.content,newpost.time,newpost.first_img from profile INNER JOIN newpost ON profile.userID=newpost.userID ORDER BY newpost.id DESC limit 10")
        new_post = cursor.fetchall()
        print(new_post)
        return {"data": new_post}
    finally:
        db.close()
