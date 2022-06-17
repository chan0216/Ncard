from model.db import con_pool


def get_cardprofile(current_user):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "select ncard.*,profile.* from ncard INNER JOIN profile on ncard.user_id = profile.user_id where ncard.user_id=%s", (current_user,))
        user = cursor.fetchone()
        if user:
            return {"data": user}
        else:
            return {"data": None}
    except Exception as e:
        return False
    finally:
        cursor.close()
        db.close()


def post_cardprofile(current_user, data):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "select user_id from ncard where user_id=%s", (current_user,))
        result = cursor.fetchone()

        if result is None:
            sql = "INSERT INTO ncard(user_id, image,  interest, club, course, country, worry, exchange, trying ,match_list) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (current_user, data["ncardImage"], data["interest"], data["club"], data["course"],
                   data["country"], data["worry"], data["exchange"], data["trying"], '[]')
            cursor.execute(sql, val)
            db.commit()
        else:
            cursor.execute("UPDATE ncard SET image=%s,interest=%s,club=%s,course=%s,country=%s, worry=%s, exchange=%s,trying=%s  where user_id=%s", (data["ncardImage"], data["interest"], data["club"], data["course"],
                                                                                                                                                     data["country"], data["worry"], data["exchange"], data["trying"], current_user))
            db.commit()
        return {"ok": True}
    except Exception as e:
        db.rollback()
        return False
    finally:
        cursor.close()
        db.close()
