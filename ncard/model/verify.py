from model.db import con_pool


def add_profile(current_user, data):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT  `user_id` from profile WHERE user_id = %s", (current_user,))
        user_profile = cursor.fetchone()
        if user_profile is None:
            cursor.execute("Insert Into profile(user_id ,realname ,gender ,school) Values( %s, %s ,%s ,%s)",
                           (current_user, data["realname"], data["gender"], data["school"]))
            db.commit()
            return {"ok": True}
        else:
            return {"error": True, "message": "重複的資料"}, 400
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()
        db.close()


def get_profile(current_user):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * from profile WHERE user_id = %s", (current_user,))
        user_profile = cursor.fetchone()
        if user_profile is not None:
            return {"data": user_profile}
        else:
            return {"data": None}
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()
