import pymysql

conn = pymysql.connect(host = "localhost", user="flask123", password="flask123", database="flask")

def DropDB():
    try:
        cursor = conn.cursor()

        drops = "drop table UserDB;"
        cursor.execute(drops)

        drops = "drop table ObjectDB;"
        cursor.execute(drops)

        drops = "drop table LocationCountDB;"
        cursor.execute(drops)

        drops = "drop table VerificationCodeDB;"
        cursor.execute(drops)

        conn.commit()
        cursor.close()
        conn.close()
    except Exception:
        pass

# 用户表
def UserDB():
    cursor = conn.cursor()
    create = "create table UserDB(" \
             "username char(32) not null," \
             "password char(32) not null," \
             "user_key char(128) not null" \
             ")"

    cursor.execute(create)

    insert = "insert into UserDB(username,password,user_key) values('lyshark','123456','1f3dsgf9834r98ug');"
    cursor.execute(insert)

    insert = "insert into UserDB(username,password,user_key) values('admin','1233','cef45f9f8480gfi5');"
    cursor.execute(insert)

    conn.commit()
    cursor.close()
    conn.close()

# 定位对象表
def ObjectDB():
    cursor = conn.cursor()
    create = "create table ObjectDB(" \
             "user_key char(128) not null," \
             "uname char(32) not null," \
             "mobile char(32) not null," \
             "ugroup char(32) not null," \
             "service_mobile char(32) not null," \
             "message_name char(255) not null," \
             "is_auth char(32) not null" \
             ")"

    cursor.execute(create)

    insert = "insert into ObjectDB(user_key,uname,mobile,ugroup,service_mobile,message_name,is_auth) " \
             "values('1f3dsgf9834r98ug','王瑞','18265477568','系统技术部','67882255','你好世界,这是一段测试文档','未授权用户');"
    cursor.execute(insert)

    insert = "insert into ObjectDB(user_key,uname,mobile,ugroup,service_mobile,message_name,is_auth) " \
             "values('cef45f9f8480gfi5','郑凯','18265477569','系统技术部','67882255','你好世界,这是一段测试文档','已授权用户');"
    cursor.execute(insert)

    conn.commit()
    cursor.close()
    conn.close()

# 定位次数费率表
def LocationCountDB():
    cursor = conn.cursor()
    create = "create table LocationCountDB(" \
             "uname char(32) not null," \
             "mobile char(32) not null unique," \
             "lat_count int not null," \
             "lat_rate float not null," \
             "trajectory_count int not null," \
             "trajectory_rate float not null," \
             "enclosure_count int not null," \
             "enclosure_rate int not null" \
             ")"

    cursor.execute(create)

    insert = "insert into LocationCountDB(uname,mobile,lat_count,lat_rate,trajectory_count,trajectory_rate,enclosure_count,enclosure_rate) " \
             "values('王瑞','18265477568',0,0,0,0,0,0);"
    cursor.execute(insert)

    insert = "insert into LocationCountDB(uname,mobile,lat_count,lat_rate,trajectory_count,trajectory_rate,enclosure_count,enclosure_rate) " \
             "values('郑凯','18265477569',0,0,0,0,0,0);"
    cursor.execute(insert)

    conn.commit()
    cursor.close()
    conn.close()

# 验证码验证表
def VerificationCodeDB():
    cursor = conn.cursor()
    create = "create table VerificationCodeDB(" \
             "mobile char(32) not null unique," \
             "code char(16) not null unique," \
             "time_stamp int not null" \
             ")"

    cursor.execute(create)

    conn.commit()
    cursor.close()
    conn.close()

# 轨迹任务表
def TrajectoryTaskDB():
    cursor = conn.cursor()
    create = "create table TrajectoryTaskDB(" \
             "uid int not null unique," \
             "task_name char(64) not null," \
             "mobile char(32) not null unique," \
             "start_time char(32) not null," \
             "end_time char(32) not null," \
             "count int not null," \
             "rate float not null" \
             ")"

    cursor.execute(create)

    conn.commit()
    cursor.close()
    conn.close()

# 轨迹历史记录表
def TrajectoryHistoryTable():
    cursor = conn.cursor()
    create = "create table TrajectoryHistoryTableDB(" \
             "mobile char(32) not null," \
             "start_time char(32) not null," \
             "end_time char(32) not null," \
             "local_time char(32) not null," \
             "x float not null," \
             "y float not null" \
             ")"

    cursor.execute(create)

    conn.commit()
    cursor.close()
    conn.close()



if __name__ == "__main__":
    UserDB()
    ObjectDB()
    LocationCountDB()
    VerificationCodeDB()