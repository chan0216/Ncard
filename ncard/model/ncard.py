from model.db import con_pool
import json


def get_ncard(current_user, today, yesterday):
    try:
        user1 = None
        user2 = None
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True, buffered=True)
        cursor.execute(
            "select `user1`,`user2` from friend where (user1 = %s OR user2 =%s ) AND date=%s", (current_user, current_user, yesterday))
        user = cursor.fetchone()
        if user is not None:
            if user['user1'] == current_user:
                user1 = user['user1']
            else:
                user2 = user['user2']
            if user1:
                cursor.execute(
                    "select `user2`,`user1_message`,`friendship` from friend where user1 = %s AND date=%s", (current_user, yesterday))
                user1 = cursor.fetchone()
                db.commit()
                invited = True if user1["user1_message"] else False
                is_friend = True if user1["friendship"] else False
                cursor.execute(
                    "select user_id,gender,name,school,image,interest,club,course,country,worry,exchange,trying from user where user_id=%s", (user1["user2"],))
                match_user = cursor.fetchone()

            else:
                cursor.execute(
                    "select `user1`,`user2_message`,`friendship` from friend where user2 = %s AND date=%s", (current_user, yesterday))
                user2 = cursor.fetchone()

                invited = True if user2["user2_message"] is not None else False
                is_friend = True if user2["friendship"] is not None else False
                cursor.execute(
                    "select user_id,gender,name,school,image,interest,club,course,country,worry,exchange,trying from user where user_id=%s", (user2["user1"],))
                match_user = cursor.fetchone()

            match_user_data = {
                "invited": invited,
                "is_friend": is_friend,
                "user_id": match_user["user_id"],
                "gender": match_user["gender"],
                "image": match_user["image"],
                "school": match_user["school"],
                "realname": match_user["name"],
                "interest": match_user["interest"],
                "club": match_user["club"],
                "course": match_user["course"],
                "country": match_user["country"],
                "worry": match_user["worry"],
                "exchange": match_user["exchange"],
                "trying": match_user["trying"],
                "date": today
            }
            return {"data": match_user_data}
        return {"data": None}
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()


def create_ncard(current_user, yesterday, now, message):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "select `user1` from friend where user1 = %s AND date=%s", (current_user, yesterday))
        user1 = cursor.fetchone()
        if user1:
            cursor.execute("UPDATE friend SET user1_message=%s WHERE user1=%s AND date=%s",
                           (message, current_user, yesterday))
            db.commit()
            cursor.execute(
                "select `id`,`user2`,`user2_message` from friend where user1 = %s  AND date=%s", (current_user, yesterday))
            user2 = cursor.fetchone()
            if user2["user2_message"] is not None:
                cursor.execute("UPDATE friend SET friendship=%s WHERE user1=%s AND date=%s",
                               (True, current_user, yesterday))
                cursor.execute("Insert Into message(ncard_id,user_id,message,time) Values(%s, %s, %s,%s)", (
                    user2["id"], current_user, message, now))
                cursor.execute("Insert Into message(ncard_id,user_id,message,time) Values(%s, %s, %s,%s)", (
                    user2["id"], user2["user2"], message, now))
                db.commit()
                return {"ok": True, "friend": True}
            else:
                return{"ok": True, "friend": False}
        else:
            cursor.execute("UPDATE friend SET user2_message=%s WHERE user2=%s AND date=%s",
                           (message, current_user, yesterday))
            db.commit()
            cursor.execute(
                "select `id`,`user1`,`user1_message` from friend where user2 = %s AND date=%s", (current_user, yesterday))
            user1 = cursor.fetchone()
            if user1["user1_message"] is not None:
                cursor.execute("UPDATE friend SET friendship=%s WHERE user2=%s AND date=%s",
                               (True, current_user, yesterday))
                cursor.execute("Insert Into message(ncard_id,user_id,message,time) Values(%s, %s, %s ,%s)", (
                    user1["id"], current_user, message, now))
                cursor.execute("Insert Into message(ncard_id,user_id,message,time) Values(%s, %s, %s , %s)", (
                    user1["id"], user1["user1"], message, now))
                db.commit()
                return {"ok": True, "friend": True}
            else:
                return{"ok": True, "friend": False}
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()
        db.close()


def user_status(current_user):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT type,match_list FROM user where user_id=%s ", (current_user, ))
        user_data = cursor.fetchone()
        if user_data["type"] == "basic":
            return {"verify_status": "basic"}
        elif user_data["type"] == "profile":
            return {"verify_status": "profile"}
        elif user_data["type"] == "ncard" and len(json.loads(user_data["match_list"])) == 0:
            return {"verify_status": "Ncard", "message": "還未配對"}
        else:
            return {"verify_status": "Ncard"}
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()
        db.close()
