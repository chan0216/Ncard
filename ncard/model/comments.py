from model.db import con_pool


def add_comment(data, current_user):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor()
        cursor.execute("Insert Into comment(post_id ,user_id ,comment ,time ) Values(%s, %s ,%s ,%s )",
                       (data["postId"], current_user, data["comment"], data["createTime"]))

        cursor.execute(
            "UPDATE post SET comment_count = comment_count + 1 WHERE id = %s;", (data["postId"],))
        db.commit()
        return {"ok": True}
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()
        db.close()


def get_comment(id):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT comment.comment,comment.time,user.gender,user.school,user.user_id from comment INNER JOIN user ON comment.user_id=user.user_id where comment.post_id=%s ORDER BY comment.id", (id,))
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
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()
