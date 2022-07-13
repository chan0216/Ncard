from ncard.model.db import con_pool


def create_user(first_index, end_index):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor()
        for i in range(first_index, end_index):
            sql = 'INSERT INTO user (username, password,signintype) VALUES ( %s, %s,%s)'
            val = (f'test{i+1}@test.com', "test", "Ncard")
            cursor.execute(sql, val)
            sql = "INSERT INTO ncard(user_id, image, interest, club, course, country, worry, exchange, trying ,match_list) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (f'{i+1}', 'https://d33yfiwdj1z4d4.cloudfront.net/108762.jpg',
                   '看劇', '熱音社', '沒有', '台灣', '疫情好嚴重', '聊天', '吃世界各地的美食', '[]')
            cursor.execute(sql, val)

            sql = "INSERT INTO profile(user_id,realname,gender,school) VAlUES (%s,%s,%s,%s)"
            val = (f'{i+1}', f'測試人員{i+1}', "F", f'國立測試大學')
            cursor.execute(sql, val)
    finally:
        print("Ncard資料輸入成功")
        db.commit()
        db.close()


create_user()
