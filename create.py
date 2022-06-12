import datetime
import random
from ncard.model.db import con_pool
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()
print(datetime.datetime.now())


def create_user():
    try:
        db = con_pool.get_connection()
        cursor = db.cursor()
        for i in range(27, 40):
            hashed_password = bcrypt.generate_password_hash(
                "123").decode('utf-8')
            sql = 'INSERT INTO user (username, password,signintype) VALUES ( %s, %s,%s)'
            val = (f'test{i+1}@test.com', hashed_password, "Ncard")
            cursor.execute(sql, val)
            sql = "INSERT INTO ncard(user_id, image, interest, club, course, country, worry, exchange, trying ,match_list) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (f'{i+1}', 'https://d33yfiwdj1z4d4.cloudfront.net/testgirl2.jpg',
                   '聽音樂、唱歌', '吉他社', '沒有', '台灣', '疫情好嚴重', '聊天', '做出好吃的料理', '[]')
            cursor.execute(sql, val)
            print("Ncard資料輸入成功")
            sql = "INSERT INTO profile(user_id,realname,gender,school) VAlUES (%s,%s,%s,%s)"
            val = (f'{i+1}', f'測試人員{i+1}', "F", f'國立測試大學')
            cursor.execute(sql, val)
    finally:
        db.commit()
        db.close()


create_user()
