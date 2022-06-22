from model.db import con_pool


def check_user(username):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT  * from user WHERE username  = %s ", (username,))
        user = cursor.fetchone()
        if user:
            return user
        else:
            return None
    except Exception as e:
        return False
    finally:
        cursor.close()
        db.close()


def create_user(username, hashed_password):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        sql = "Insert Into user(username,password) Values( %s,%s)"
        val = (username, hashed_password)
        cursor.execute(sql, val)
        db.commit()
        cursor.execute(
            "SELECT  `user_id` from user WHERE username = %s", (username,))
        user_id = cursor.fetchone()
        return user_id
    except Exception as e:
        db.rollback()
        return False
    finally:
        cursor.close()
        db.close()
