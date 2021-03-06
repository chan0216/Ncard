from model.db import con_pool


def add_new_post(current_user, data, first_img):
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


def get_new_post(page):
    try:
        render_num = 10
        render_index = page * render_num
        db = con_pool.get_connection()
        next_page = None
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT profile.gender,profile.school,newpost.id,newpost.title,newpost.content,newpost.time,newpost.first_img,newpost.like_count,newpost.comment_count from profile INNER JOIN newpost ON profile.user_id=newpost.user_id ORDER BY newpost.id DESC limit %s,%s", (render_index, render_num+1))
        new_posts = cursor.fetchall()
        if len(new_posts) == 11:
            next_page = page+1
            new_posts.pop(10)
        post_list = []
        for post in new_posts:
            post_data = {
                "comment_count":  post["comment_count"],
                "content": post["content"],
                "first_img": post["first_img"],
                "gender":  post["gender"],
                "id": post["id"],
                "like_count": post["like_count"],
                "school": post["school"],
                "time": post["time"],
                "title": post["title"],
            }
            post_list.append(post_data)
        return {"data": post_list, "nextPage": next_page}
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
                "time": post["time"].strftime('%m???%d??? %H:%M'),
                "comment_count": post["comment_count"],
                "like_count": post["like_count"],
                "like_post": like_post
            }
            return {"data": post_data}

        else:
            return {"error": True, "message": "?????????????????????"}, 400
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
