from model.db import con_pool


def get_all_friends(current_user):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True, buffered=True)
        query = ("SELECT friend.*,ncard.*,profile.* FROM friend INNER JOIN ncard on friend.user1=ncard.user_id INNER JOIN profile on friend.user1=profile.user_id WHERE (friend.user1=%s OR friend.user2=%s) AND (friend.friendship IS true)  UNION ALL SELECT friend.*,ncard.*,profile.* FROM friend INNER JOIN ncard on friend.user2=ncard.user_id INNER JOIN profile on friend.user2=profile.user_id WHERE (friend.user1=%s OR friend.user2=%s) AND (friend.friendship IS true)")
        data = (current_user, current_user, current_user, current_user)
        cursor.execute(query, data)
        all_user = cursor.fetchall()
        if all_user:
            friend_list = []
            for index in range(len(all_user)):
                if all_user[index]['user_id'] != current_user:
                    data = {
                        "user_id": all_user[index]["user_id"],
                        "realname": all_user[index]["realname"],
                        "school": all_user[index]["school"],
                        "image": all_user[index]["image"]
                    }
                    friend_list.append(data)
            return {"data": friend_list}
        else:
            return {"data": None}
    finally:
        cursor.close()
        db.close()


def get_friend(id, current_user):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(buffered=True, dictionary=True)
        cursor.execute(
            "select ncard.*,profile.* from ncard inner join profile on ncard.user_id=profile.user_id where ncard.user_id=%s", (id,))
        friend = cursor.fetchone()
        cursor.execute(
            "select ncard_id,user_id from message where ncard_id =(select id from friend where (user1=%s and user2=%s  and friendship IS true) or (user1=%s and user2=%s  and friendship IS true) ) group by user_id", (id, current_user, current_user, id))
        users = cursor.fetchall()
        users_list = []
        ncard_list = []
        for user in users:
            users_list.append(user["user_id"])
            ncard_list.append(user["ncard_id"])
        if current_user not in users_list:
            return{"error": True, "message": "此人不是你的好友"}, 400
        else:
            friend_data = {
                "ncardId": ncard_list[0],
                "friendId": friend["user_id"],
                "friendName": friend["realname"],
                "school": friend["school"],
                "image": friend["image"],
                "interest": friend["interest"],
                'club': friend['club'],
                'course': friend['course'],
                'country': friend['country'],
                'worry': friend['worry'],
                "exchange": friend["exchange"],
                'trying': friend["trying"]
            }
            return {"data": friend_data}
    finally:
        cursor.close()
        db.close()
