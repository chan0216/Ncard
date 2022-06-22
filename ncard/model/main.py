from model.db import con_pool


def redirect_msg(current_user):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(buffered=True)
        cursor.execute(
            "select `ncard_id` from message where user_id=%s ORDER BY id desc limit 1", (current_user,))
        last_ncardid = cursor.fetchone()
        return last_ncardid
    except Exception as e:
        return False
    finally:
        cursor.close()
        db.close()


def handle_send_message(data, now):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor()
        cursor.execute(
            "insert into message(ncard_id,user_id,message,time) VALUES (%s, %s, %s, %s)", (data["room"], data["userId"], data["message"], now))
        db.commit()
        return {"ok": True}
    except Exception as e:
        db.rollback()
        return False
    finally:
        cursor.close()
        db.close()
