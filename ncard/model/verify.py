from model.db import con_pool


def add_profile(current_user, data):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT  `type` from user WHERE user_id = %s", (current_user,))
        user_type = cursor.fetchone()
        if user_type["type"] == "basic":
            cursor.execute("Update user set name=%s,gender=%s,school=%s,type=%s where user_id=%s",
                           (data["fullname"], data["gender"], data["school"], "profile", current_user))
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
            "SELECT name,gender,school,type from user WHERE user_id = %s", (current_user,))
        user_data = cursor.fetchone()
        if user_data["type"] == "ncard" or user_data["type"] == "profile":
            return {"data": user_data}
        else:
            return {"data": None}
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()
