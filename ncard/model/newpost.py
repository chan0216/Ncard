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
            "SELECT profile.gender,profile.school,newpost.id,newpost.title,newpost.content,newpost.time,newpost.first_img,newpost.like_count,newpost.comment_count from profile INNER JOIN newpost ON profile.user_id=newpost.user_id ORDER BY newpost.id DESC")
        new_post = cursor.fetchall()
        return {"data": new_post}
    except Exception as e:
        return False
    finally:
        cursor.close()
        db.close()


def get_hot_articles():
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT profile.gender,profile.school,newpost.id,newpost.title,newpost.content,newpost.time,newpost.first_img,newpost.like_count,newpost.comment_count from profile INNER JOIN newpost ON profile.user_id=newpost.user_id ORDER BY like_count DESC")
        new_post = cursor.fetchall()
        return {"data": new_post}
    except Exception as e:
        return False
    finally:
        cursor.close()
        db.close()


def get_article(id, current_user):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT profile.user_id,profile.gender,profile.school,newpost.title,newpost.content,newpost.time,newpost.comment_count,newpost.like_count from profile INNER JOIN newpost ON profile.user_id=newpost.user_id where newpost.id=%s", (id,))
        post = cursor.fetchone()
        like_post = False
        if current_user:
            cursor.execute(
                "select * from user_post_like where user_id=%s and post_id=%s", (current_user, id))
            like = cursor.fetchone()
            if like:
                like_post = True
        if post:
            post_data = {
                "user_id": post["user_id"],
                "gender": post["gender"],
                "school": post["school"],
                "title": post["title"],
                "content": post["content"],
                "time": post["time"].strftime('%m月%d日 %H:%M'),
                "comment_count": post["comment_count"],
                "like_count": post["like_count"],
                "like_post": like_post
            }
            return {"data": post_data}

        else:
            return {"error": True, "message": "沒有這篇文章喔"}, 400
    except Exception as e:
        return False
    finally:
        cursor.close()
        db.close()


def patch_post_like(post_id, current_user):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor()
        cursor.execute(
            "select * from user_post_like where user_id=%s and post_id=%s", (current_user, post_id))
        like = cursor.fetchone()
        if like:
            cursor.execute(
                "DELETE FROM user_post_like WHERE user_id=%s and post_id=%s", (current_user, post_id))
            cursor.execute(
                "select like_count from newpost where id=%s", (post_id,))
            like_count = cursor.fetchone()
            like_count = like_count[0]
            like_count -= 1
            cursor.execute(
                "UPDATE newpost SET like_count=%s WHERE id=%s", (like_count, post_id))
        else:
            cursor.execute(
                "insert into user_post_like(user_id,post_id) values (%s,%s)", (current_user, post_id))
            cursor.execute(
                "select like_count from newpost where id=%s", (post_id,))
            like_count = cursor.fetchone()
            like_count = like_count[0]
            like_count += 1
            cursor.execute(
                "UPDATE newpost SET like_count=%s WHERE id=%s", (like_count, post_id))
        return {"like_count": like_count}
    except Exception as e:
        db.rollback()
        return False
    finally:
        db.commit()
        cursor.close()
        db.close()


def add_comment(data, current_user):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor()
        cursor.execute("Insert Into comment(post_id ,user_id ,comment ,time ) Values(%s, %s ,%s ,%s )",
                       (data["postId"], current_user, data["comment"], data["createTime"]))

        cursor.execute(
            "UPDATE newpost SET comment_count = comment_count + 1 WHERE id = %s;", (data["postId"],))
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
