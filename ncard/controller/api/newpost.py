from venv import create
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
    try:

        data = request. json
        first_img = None
        imgs = re.search(
            r"(https://.(.*?)[-\w]+\.(jpg|gif|png|jpeg$))", data["postText"])
        if imgs:
            first_img = imgs.group()
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("Insert Into newpost(user_id ,title ,content ,time ,first_img) Values(%s, %s ,%s ,%s ,%s)",
                       (current_user, data["postTitle"], data["postText"], data["timenow"], first_img))
        db.commit()
        return {"ok": True}
    # except:
    #     db.rollback()
    #     return {"error": True},500
    # finally:
    #     db.close()
    finally:
        cursor.close()
        db.close()


@newpost_blueprint.route("/api/newpost", methods=["GET"])
def getnewpost():
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT profile.gender,profile.school,newpost.id,newpost.title,newpost.content,newpost.time,newpost.first_img from profile INNER JOIN newpost ON profile.user_id=newpost.user_id ORDER BY newpost.id DESC limit 10")
        new_post = cursor.fetchall()
        return {"data": new_post}
    finally:
        cursor.close()
        db.close()


@newpost_blueprint.route("/api/post/<id>", methods=["GET"])
def article(id):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT profile.user_id,profile.gender,profile.school,newpost.title,newpost.content,newpost.time from profile INNER JOIN newpost ON profile.user_id=newpost.user_id where newpost.id=%s", (id,))
        post = cursor.fetchone()
        if post:
            return {"data": post}
        else:
            return {"error": True, "message": "沒有這篇文章喔"}, 400
    finally:
        cursor.close()
        db.close()


@newpost_blueprint.route("/api/comment", methods=["POST"])
@token_required
def post_comment(current_user):
    try:
        data = request. json
        db = con_pool.get_connection()
        cursor = db.cursor()
        cursor.execute("Insert Into comment(post_id ,user_id ,comment ,time ) Values(%s, %s ,%s ,%s )",
                       (data["postId"], current_user, data["comment"], data["createTime"]))
        return {"ok": True}
    except:
        db.rollback()
        return {"error": True}
    finally:
        db.commit()
        cursor.close()
        db.close()


@newpost_blueprint.route("/api/comment/<id>", methods=["GET"])
def get_comment(id):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT comment.comment,comment.time, profile.* from comment INNER JOIN profile ON comment.user_id=profile.user_id where comment.post_id=%s ORDER BY comment.id", (id,))
        all_comment = cursor.fetchall()
        if all_comment:
            comment_list = []
            for item in range(len(all_comment)):
                date_time = all_comment[item]["time"].strftime(
                    "%Y/%m/%d %H:%M:%S")
                data = {
                    "user_id":  all_comment[item]["user_id"],
                    "gender": all_comment[item]["gender"],
                    "school": all_comment[item]["school"],
                    "comment": all_comment[item]["comment"],
                    "create_time": date_time
                }
                comment_list.append(data)
            return {"data": comment_list}
        else:
            return {"data": None}
    finally:
        cursor.close()
        db.close()
