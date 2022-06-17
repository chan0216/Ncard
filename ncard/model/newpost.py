from model.db import con_pool


def add_newpost(current_user, data, first_img):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("Insert Into newpost(user_id ,title ,content ,time ,first_img) Values(%s, %s ,%s ,%s ,%s)",
                       (current_user, data["postTitle"], data["postText"], data["timenow"], first_img))
        db.commit()
        return {"ok": True}
    except Exception as e:
        db.rollback()
        return False
    finally:
        cursor.close()
        db.close()


def get_newpost():
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT profile.gender,profile.school,newpost.id,newpost.title,newpost.content,newpost.time,newpost.first_img from profile INNER JOIN newpost ON profile.user_id=newpost.user_id ORDER BY newpost.id DESC limit 10")
        new_post = cursor.fetchall()
        return {"data": new_post}
    except Exception as e:
        return False
    finally:
        cursor.close()
        db.close()


def get_article(id):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT profile.user_id,profile.gender,profile.school,newpost.title,newpost.content,newpost.time from profile INNER JOIN newpost ON profile.user_id=newpost.user_id where newpost.id=%s", (id,))
        post = cursor.fetchone()
        if post:
            return {"data": post}
        else:
            return {"error": True, "message": "沒有這篇文章喔"}, 400
    except Exception as e:
        return False
    finally:
        cursor.close()
        db.close()


def add_comment(data, current_user):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor()
        cursor.execute("Insert Into comment(post_id ,user_id ,comment ,time ) Values(%s, %s ,%s ,%s )",
                       (data["postId"], current_user, data["comment"], data["createTime"]))
        db.commit()
        return {"ok": True}
    except Exception as e:
        db.rollback()
        return False
    finally:
        cursor.close()
        db.close()


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
