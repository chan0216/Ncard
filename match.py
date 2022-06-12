import random
import mysql.connector.pooling
from decouple import config
import json
from datetime import date, timedelta
import time


def matchuser():
    today = date.today()
    yesterday = today - timedelta(days=1)
    dby = yesterday - timedelta(days=1)
    con_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name='connection_pool',
        pool_size=10,
        host=config('host', default=''),
        database=config('database', default=''),
        user=config('user', default=''),
        password=config('password', default='')
    )

    try:
        start_time = time.time()
        user_list = []
        match_list = []
        db = con_pool.get_connection()
        cursor = db.cursor()
        cursor.execute(
            'DELETE FROM friend WHERE friendship IS NULL AND date=%s', (dby,))
        db.commit()
        cursor.execute("SELECT user_id,match_list From ncard")
        all_users = cursor.fetchall()
        for user in all_users:
            user_list.append(user[0])
            match_list.append(json. loads(user[1]))
        print(user_list, match_list)
        user_count = len(user_list)
        if (user_count % 2) != 0:
            del user_list[0]
            del match_list[0]
        for user_index in range(len(user_list)):
            user_index = 0
            user_id = user_list[user_index]
            user_list.remove(user_id)
            matching_list = match_list[user_index]
            match_list.remove(matching_list)
            match_index = random.randrange(len(user_list))
            pair_user2 = user_list[match_index]
            while (pair_user2 in matching_list):
                match_index = random.randrange(len(user_list))
                pair_user2 = user_list[match_index]
            user_list.remove(pair_user2)
            match_list.remove(match_list[match_index])
            print(user_id, pair_user2)
            cursor.execute(
                "UPDATE ncard SET match_list=JSON_ARRAY_APPEND (match_list, '$' , %s) where user_id=%s", (user_id, pair_user2))
            cursor.execute(
                "UPDATE ncard SET match_list=JSON_ARRAY_APPEND (match_list, '$' , %s) where user_id=%s", (pair_user2, user_id))
            sql = 'INSERT INTO friend (user1, user2, date) VALUES ( %s, %s, %s)'
            val = (user_id, pair_user2, today)
            cursor.execute(sql, val)
            db.commit()
    except:
        db.rollback()
    finally:
        with open('process.txt', 'a') as outFile:
            outFile.write('Process time: %f sec' % (time.time() - start_time))
        print('Process time: %f sec' % (time.time() - start_time))
        cursor.close()
        db.close()


matchuser()
