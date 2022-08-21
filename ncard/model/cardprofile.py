from model.db import con_pool
from model.model import redis


def get_profile(current_user):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "select name,gender,school,image,interest,club,course,country,worry,exchange,trying from user where user_id=%s", (current_user,))
        user = cursor.fetchone()
        if user:
            return {"data": user}
        else:
            return {"data": None}
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()


def post_profile(current_user, data):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "select type from user where user_id=%s", (current_user,))
        user_data = cursor.fetchone()

        if user_data["type"] == "profile":
            sql = "UPDATE user SET type=%s,image=%s,interest=%s,club=%s,course=%s,country=%s, worry=%s, exchange=%s,trying=%s,match_list=%s where user_id=%s"
            val = ("ncard", data["ncardImage"], data["interest"], data["club"], data["course"],
                   data["country"], data["worry"], data["exchange"], data["trying"], '[]', current_user)
            cursor.execute(sql, val)
            db.commit()
        else:
            cursor.execute("UPDATE user SET image=%s,interest=%s,club=%s,course=%s,country=%s, worry=%s, exchange=%s,trying=%s where user_id=%s", (
                data["ncardImage"], data["interest"], data["club"], data["course"], data["country"], data["worry"], data["exchange"], data["trying"], current_user))
            card_id = f"card_{current_user}"
            redis.delete(card_id)
            db.commit()
        return {"ok": True}
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()
        db.close()
