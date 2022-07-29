import random
import mysql.connector.pooling
from decouple import config
import json
from datetime import date, timedelta
import time
import logging
logging.basicConfig(level=logging.DEBUG,
                    datefmt='%Y-%m-%d %H:%M',
                    handlers=[logging.FileHandler('process.log', 'w', 'utf-8'), ])


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
        pair_array = []
        user_list = []
        match_list = []
        db = con_pool.get_connection()
        cursor = db.cursor()
        cursor.execute(
            'DELETE FROM friend WHERE friendship IS NULL AND date=%s', (dby,))
        db.commit()
        select_time = time.time()
        # 取出今日要配對的user_id
        cursor.execute("SELECT user_id,match_list From ncard")
        all_users = cursor.fetchall()
        logging.debug('取出 user_id time: %f sec' % (time.time() - select_time))
        for user in all_users:
            user_list.append(user[0])
            match_list.append(json. loads(user[1]))
        # 若配對人數是基數，則移除第一位測試帳號
        user_count = len(user_list)
        if (user_count % 2) != 0:
            del user_list[0]
            del match_list[0]
            user_count -= 1
        # 配對程序
        for user_index in range(len(user_list)):
            user_index = 0
            user_id = user_list[user_index]
            user_list.remove(user_id)
            matching_list = match_list[user_index]
            match_list.remove(matching_list)
            # 隨機抽取一位使用者，與曾經配對過的陣列比對，若配對過則重新配對
            match_index = random.randrange(len(user_list))
            pair_user = user_list[match_index]
            while (pair_user in matching_list):
                match_index = random.randrange(len(user_list))
                pair_user = user_list[match_index]
            # 將已經配對過的user_id剔除
            user_list.remove(pair_user)
            match_list.remove(match_list[match_index])
            pair_array.append((user_id, pair_user, today))
            update_time = time.time()
            cursor.execute(
                "UPDATE ncard SET match_list=JSON_ARRAY_APPEND (match_list, '$' , %s) where user_id=%s", (user_id, pair_user))
            cursor.execute(
                "UPDATE ncard SET match_list=JSON_ARRAY_APPEND (match_list, '$' , %s) where user_id=%s", (pair_user, user_id))
            db.commit()
            if not user_list:
                break
            logging.debug('更新配對陣列 time : %f sec' % (time.time() - update_time))
        insert_time = time.time()
        stmt = "INSERT INTO friend (user1, user2, date) VALUES ( %s, %s, %s)"
        cursor.executemany(stmt, pair_array)
        db.commit()
        logging.debug('insert 今日配對 time: %f sec' %
                      (time.time() - insert_time))
    except:
        db.rollback()
    finally:
        logging.debug('match Process time: %f sec' %
                      (time.time() - start_time))
        cursor.close()
        db.close()


matchuser()
