from model.db import con_pool


def get_room(current_user):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor()
        cursor.execute(
            "select id from friend WHERE (user1 = %s or user2 = %s) AND friendship IS true", (current_user, current_user))
        rooms_id = cursor.fetchall()
        if rooms_id:
            roomlist = []
            for room_id in rooms_id:
                roomlist.append(room_id)
            return {"data": roomlist}
        else:
            return {"data": None}
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()


def get_friends(current_user):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "select * from (select * from message ORDER BY id DESC limit 0,18446744073709551615 ) as msg where ncard_id In (select ncard_id from message where user_id=%s ) GROUP BY ncard_id  ORDER BY id DESC",
            (current_user,))
        last_messages = cursor.fetchall()
        friends_list = []
        for info in last_messages:
            room_id = info["ncard_id"]
            cursor.execute(
                "select user_id from message where ncard_id=%s group by user_id", (room_id,))
            users = cursor.fetchall()
            users_list = []
            for user in users:
                users_list.append(user["user_id"])
            users_list.remove(current_user)
            friend_id = users_list[0]
            cursor.execute(
                "select ncard.image,profile.realname from ncard inner join profile on ncard.user_id=profile.user_id where ncard.user_id=%s", (friend_id,))
            friend = cursor.fetchone()
            friends_data = {
                "name": friend["realname"],
                "image": friend["image"],
                "message": info["message"],
                "time": info["time"].strftime("%m-%d %H:%M"),
                "room_id": info["ncard_id"]
            }
            friends_list.append(friends_data)
        return {"data": friends_list}
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()


def get_chats(page, next_page, id, current_user):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(buffered=True, dictionary=True)
        cursor.execute(
            "select user_id from message where ncard_id=%s group by user_id", (id,))
        users = cursor.fetchall()
        users_list = []
        for user in users:
            users_list.append(user["user_id"])
        if current_user not in users_list:
            return{"error": True, "message": "這邊不是你的聊天室"}, 400
        users_list.remove(current_user)
        # 抓出朋友的id
        friend_id = users_list[0]
        # current_user data
        cursor.execute(
            "select profile.user_id,profile.realname,ncard.image from profile inner join ncard on profile.user_id=ncard.user_id where profile.user_id=%s", (current_user, ))
        user = cursor.fetchone()
        user_data = {
            "user_id": user["user_id"],
            "name": user["realname"],
            "image": user["image"]
        }
        cursor.execute(
            "select profile.user_id,profile.realname,ncard.image from profile inner join ncard on profile.user_id=ncard.user_id where profile.user_id=%s", (friend_id, ))
        friend = cursor.fetchone()
        friend_data = {
            "friend_id": friend["user_id"],
            "name": friend["realname"],
            "image": friend["image"]
        }
        cursor.execute(
            "select user_id,message,time from message where ncard_id = %s ", (id, ))
        messages = cursor.fetchall()
        cursor.execute(
            "select user_id,message,time from message where ncard_id = %s", (id, ))
        next_messages = cursor.fetchall()
        if not next_messages:
            next_page = None
        message_list = []
        for message in messages:
            message_data = {
                "userId": message["user_id"],
                "message": message["message"],
                "time": message["time"].strftime("%m-%d %H:%M")
            }
            message_list.append(message_data)
        data = {
            "user": user_data,
            "friend": friend_data,
            "messages": message_list,
            "nextPage": next_page
        }
        return {"data": data}
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()
