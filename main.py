from flask import Flask, request
import json,sqlite3
import random,string
import time,datetime
import logging
import threading
import requests
import xmltodict

import pymysql

# 手机号规则
TelList = ["130", "131", "132", "145", "155", "156", "175", "176", "185", "186", "166", "146", "10646"]

# 数据库文件
sql_file = "database.db"

#conn = pymysql.connect(host = "localhost", user="root", password="123456", database="location")

LOG_FORMAT = "日志时间: %(asctime)s 级别: %(levelname)s ---> %(message)s"
logging.basicConfig(filename='message.log', level=logging.WARNING, format=LOG_FORMAT)

app = Flask(__name__, template_folder="templates")

# 查询SQL
def select_sql(sql):
    try:
        conn = sqlite3.connect(sql_file)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        return cursor.fetchall()
    except Exception:
        app.logger.warning("查询SQL语句执行异常")
        return False

# 插入新记录SQL
def insert_sql(sql):
    try:
        conn = sqlite3.connect(sql_file)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return True
    except Exception:
        app.logger.warning("插入SQL语句执行异常")
        return False

# 更新SQL
def update_sql(sql):
    try:
        conn = sqlite3.connect(sql_file)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return True
    except Exception:
        app.logger.warning("更新SQL语句执行异常")
        return False

# 删除记录SQL
def delete_sql(sql):
    try:
        conn = sqlite3.connect(sql_file)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return True
    except Exception:
        app.logger.warning("删除SQL语句执行异常")
        return False

# 生成一个指定长度的随机字符串
def generate_random_str(randomlength=32):
    str_list = [random.choice(string.digits + string.ascii_letters) for i in range(randomlength)]
    random_str = ''.join(str_list)
    return random_str

# ----------------------------------------------------------------------------------------------------------------------
# 登录 + 验证 + 登出
# ----------------------------------------------------------------------------------------------------------------------
# 用户登录
@app.route('/login', methods=['POST'])
def login():
    return_dict = {'status': '0', 'token': 'none'}

    if request.method == "POST":
        if len(request.get_data()) != 0:
            try:
                username = request.values.get("username")
                password = request.values.get("password")

                # 验证账号密码是否正确
                ref_data = select_sql("select * from UserDB;")

                # 当查询不为假则执行
                if ref_data != False:
                    for data in ref_data:
                        # 正确返回key
                        if (data[0] == username) and (data[1] == password):
                            return_dict["status"] = "1"
                            return_dict["token"] = data[2]
                            return json.dumps(return_dict, ensure_ascii=False)
                else:
                    return_dict["status"] = "0"
                    return_dict["token"] = "查询记录失败"
                    app.logger.warning("用户登录：查询记录失败")
                    return json.dumps(return_dict, ensure_ascii=False)

            except Exception:
                return_dict["status"] = "0"
                return_dict["token"] = "接口异常"
                app.logger.warning("用户登录：接口异常")
                return json.dumps(return_dict, ensure_ascii=False)
        else:
            return_dict["status"] = "0"
            return_dict["token"] = "传入参数不能为空"
            app.logger.warning("用户登录：传入参数不能为空")
            return json.dumps(return_dict, ensure_ascii=False)

    return_dict["status"] = "0"
    return_dict["token"] = "用户名或密码错误"
    app.logger.warning("用户登录：用户名或密码错误")
    return json.dumps(return_dict, ensure_ascii=False)

# 判断是否登录
@app.route('/is_login',methods=['POST'])
def is_login():
    return_dict = {'status': '0','user': 'none'}

    if request.method == "POST":
        if len(request.get_data()) != 0:
            try:
                key = request.values.get("token")
                # 验证是否登录
                ref_data = select_sql("select * from UserDB;")
                if ref_data != False:
                    for data in ref_data:
                        if(data[2] == key):
                            return_dict['status'] = "1"
                            return_dict['user'] = data[0]
                            return json.dumps(return_dict, ensure_ascii=False)
                else:
                    return_dict["status"] = "0"
                    return_dict["user"] = "查询记录失败"
                    app.logger.warning("判断是否登录：查询记录失败")
                    return json.dumps(return_dict, ensure_ascii=False)

            except Exception:
                return_dict["status"] = "0"
                return_dict["user"] = "接口异常"
                app.logger.warning("判断是否登录：接口异常")
                return json.dumps(return_dict, ensure_ascii=False)
        else:
            return_dict['status'] = "0"
            return_dict['user'] = "传入参数不能为空"
            app.logger.warning("判断是否登录：传入参数不能为空")
            return json.dumps(return_dict, ensure_ascii=False)

    return_dict["status"] = "0"
    return_dict["user"] = "密钥失效,请重新登录"
    app.logger.warning("判断是否登录：密钥失效,请重新登录")
    return json.dumps(return_dict, ensure_ascii=False)

# 刷新用户Token
@app.route('/flush_token',methods=['POST'])
def flush_token():
    return_dict = {'status': '0','message': 'none'}

    if request.method == "POST":
        if len(request.get_data()) != 0:
            try:
                key = request.values.get("token")
                uuid = generate_random_str(32)

                # 用户登出 更新第一张表中的Key
                if update_sql("update UserDB set user_key='{}' where user_key='{}'".format(uuid, key)) != False:
                    # 更新第二张表中的Key
                    if update_sql("update ObjectDB set user_key='{}' where user_key='{}'".format(uuid, key)) != False:
                        return_dict["status"] = "1"
                        return_dict["message"] = "已刷新"
                        return json.dumps(return_dict, ensure_ascii=False)
            except Exception:
                return_dict["status"] = "0"
                return_dict["message"] = "接口异常"
                app.logger.warning("刷新用户Token：接口异常")
                return json.dumps(return_dict, ensure_ascii=False)
        else:
            return_dict['status'] = "0"
            return_dict['message'] = "传入参数不能为空"
            app.logger.warning("刷新用户Token：传入参数不能为空")
            return json.dumps(return_dict, ensure_ascii=False)

    return_dict["status"] = "0"
    return_dict["message"] = "未知错误"
    app.logger.warning("刷新用户Token：未知错误")
    return json.dumps(return_dict, ensure_ascii=False)


# ----------------------------------------------------------------------------------------------------------------------
# 定位对象相关接口
# ----------------------------------------------------------------------------------------------------------------------

# 创建定位对象
@app.route('/create_object',methods=['POST'])
def create_object():
    return_dict = {'status': '0','message': 'none'}
    if request.method == "POST":
        # 验证参数是否一致
        if len(request.get_data()) != 0 and len(request.values) == 6:
            key = request.values.get("token")
            uname = request.values.get("uname")
            mobile = request.values.get("mobile")
            ugroup = request.values.get("ugroup")
            service_mobile = request.values.get("service_mobile")
            message_name = request.values.get("message_name")

            # 验证是否是联通手机号
            if mobile.strip()[0:3] in TelList or mobile.strip()[0:5] in TelList:

                # 查询UserDB表内是否存在用户传入的key
                ref_data = select_sql("select user_key from UserDB where user_key='{}';".format(key))
                if len(ref_data) != 0 and ref_data != False:

                    # 检查表内是否存在手机号
                    ref_mobile_data = select_sql("select count(mobile) from ObjectDB where mobile='{}'".format(mobile))
                    if int(ref_mobile_data[0][0]) == 0:

                        # 开始构建插入数据库语句
                        insert_ref = "insert into ObjectDB(user_key,uname,mobile,ugroup,service_mobile,message_name,is_auth) " \
             "values('{}','{}','{}','{}','{}','{}','未授权用户');".format(key,uname,mobile,ugroup,service_mobile,message_name)
                        insert_ref_flag = insert_sql(insert_ref)

                        if insert_ref_flag == True:

                            # 同步插入计数计费表
                            insert_sql("insert into LocationCountDB(uname,mobile,lat_count,lat_rate,trajectory_count,trajectory_rate,enclosure_count,enclosure_rate) " \
                                     "values('{}','{}',0,0,0,0,0,0);".format(uname,mobile))

                            return_dict["status"] = "1"
                            return_dict["message"] = "已新增定位对象"
                            return json.dumps(return_dict, ensure_ascii=False)
                        else:
                            return_dict["status"] = "0"
                            return_dict["message"] = "新增定位对象失败"
                            app.logger.warning("创建定位对象：新增定位对象失败")
                            return json.dumps(return_dict, ensure_ascii=False)

                    else:
                        return_dict["status"] = "0"
                        return_dict["message"] = "手机号已存在,无法继续创建"
                        app.logger.warning("创建定位对象：手机号已存在,无法继续创建")
                        return json.dumps(return_dict, ensure_ascii=False)
                else:
                    return_dict["status"] = "0"
                    return_dict["message"] = "传入Key密钥对错误"
                    app.logger.warning("创建定位对象：传入Key密钥对错误")
                    return json.dumps(return_dict, ensure_ascii=False)
            else:
                return_dict["status"] = "0"
                return_dict["message"] = "请输入联通手机号"
                app.logger.warning("创建定位对象：请输入联通手机号")
                return json.dumps(return_dict, ensure_ascii=False)
        else:
            return_dict["status"] = "0"
            return_dict["message"] = "传入参数错误"
            app.logger.warning("创建定位对象：传入参数错误")
            return json.dumps(return_dict, ensure_ascii=False)

    return_dict["status"] = "0"
    return_dict["message"] = "未知错误"
    app.logger.warning("创建定位对象：未知错误")
    return json.dumps(return_dict, ensure_ascii=False)

# 查询所有定位对象
@app.route('/select_all_object',methods=['POST'])
def select_all_object():
    return_dict = {'status': '0','count': '0', 'message': 'none'}
    if request.method == "POST":
        # 验证参数是否一致
        if len(request.get_data()) != 0 and len(request.values) == 1:
            key = request.values.get("token")
            # 查询UserDB表内是否存在用户传入的key
            ref_data = select_sql("select user_key from UserDB where user_key='{}';".format(key))
            if len(ref_data) != 0 and ref_data != False:
                # 定义组合模板
                object_list = []

                ref_data_object = select_sql("select * from ObjectDB;")
                if ref_data_object != False:

                    # 循环组合成JSON
                    for item in ref_data_object:
                        li = [item[1],item[2],item[3],item[4],item[5]]
                        object_list.append(li)

                    return_dict["status"] = "1"
                    return_dict["count"] = len(object_list)
                    return_dict["message"] = object_list
                    return json.dumps(return_dict, ensure_ascii=False)

            else:
                return_dict["status"] = "0"
                return_dict["count"] = "0"
                return_dict["message"] = "查询异常"
                app.logger.warning("查询所有定位对象：查询异常")
                return json.dumps(return_dict, ensure_ascii=False)

        else:
            return_dict["status"] = "0"
            return_dict["count"] = "0"
            return_dict["message"] = "传入参数错误"
            app.logger.warning("查询所有定位对象：传入参数错误")
            return json.dumps(return_dict, ensure_ascii=False)

    return_dict["status"] = "0"
    return_dict["count"] = "0"
    return_dict["message"] = "未知错误"
    app.logger.warning("查询所有定位对象：未知错误")
    return json.dumps(return_dict, ensure_ascii=False)

# 删除定位对象
@app.route('/delete_object',methods=['POST'])
def delete_object():
    return_dict = {'status': '0','message': 'none'}
    if request.method == "POST":
        # 验证参数是否一致
        if len(request.get_data()) != 0 and len(request.values) == 2:
            key = request.values.get("token")
            mobile = request.values.get("mobile")

            # 验证是否是联通手机号
            if mobile.strip()[0:3] in TelList or mobile.strip()[0:5] in TelList:
                # 查询UserDB表内是否存在用户传入的key
                ref_data = select_sql("select user_key from UserDB where user_key='{}';".format(key))
                if len(ref_data) != 0 and ref_data != False:
                    '''
                        # 查询定位对象是否存在
                        select_ref = select_sql("select mobile from ObjectDB wehere mobile='{}'".format(mobile))
    
                        print(select_ref)
                        if select_ref == False:
                            return_dict["status"] = "0"
                            return_dict["message"] = "定位对象不存在"
                            return json.dumps(return_dict, ensure_ascii=False)
                        else:
                            # 存在则直接删除该定位对象
                            ref = delete_sql("delete from ObjectDB where mobile = '{}'".format(mobile))
                            if ref == True:
                                return_dict["status"] = "1"
                                return_dict["message"] = "定位对象已删除"
                                return json.dumps(return_dict, ensure_ascii=False)
                    '''
                    ref = delete_sql("delete from ObjectDB where mobile = '{}'".format(mobile))
                    if ref == True:
                        return_dict["status"] = "1"
                        return_dict["message"] = "已处理"
                        return json.dumps(return_dict, ensure_ascii=False)

            else:
                return_dict["status"] = "0"
                return_dict["message"] = "请输入联通手机号"
                app.logger.warning("删除定位对象：请输入联通手机号")
                return json.dumps(return_dict, ensure_ascii=False)

        else:
            return_dict["status"] = "0"
            return_dict["message"] = "传入参数错误"
            app.logger.warning("删除定位对象：传入参数错误")
            return json.dumps(return_dict, ensure_ascii=False)

    return_dict["status"] = "0"
    return_dict["message"] = "未知错误"
    app.logger.warning("删除定位对象：未知错误")
    return json.dumps(return_dict, ensure_ascii=False)

# ----------------------------------------------------------------------------------------------------------------------
# 用户组相关接口
# ----------------------------------------------------------------------------------------------------------------------

# 查询所有用户组
@app.route('/select_all_group',methods=['POST'])
def select_all_group():
    return_dict = {'status': '0','count': 'none', 'message': 'none'}
    if request.method == "POST":
        # 验证参数是否一致
        if len(request.get_data()) != 0 and len(request.values) == 1:
            key = request.values.get("token")
            # 查询UserDB表内是否存在用户传入的key
            ref_data = select_sql("select user_key from UserDB where user_key='{}';".format(key))
            if len(ref_data) != 0 and ref_data != False:
                # 定义组合模板
                object_list = []

                # 查询组并去重后放入ref
                ref_select_data = select_sql("select ugroup from ObjectDB;")
                if ref_select_data != False:
                    for each in ref_select_data:
                        object_list.append(each[0])

                    ref = list( set(object_list) )
                    ref_count = len(set(object_list))

                    # 返回系统部门
                    return_dict["status"] = "1"
                    return_dict["count"] = ref_count
                    return_dict["message"] = ref
                    return json.dumps(return_dict, ensure_ascii=False)

                else:
                    return_dict["status"] = "0"
                    return_dict["message"] = "查询异常"
                    app.logger.warning("查询所有用户组：查询异常")
                    return json.dumps(return_dict, ensure_ascii=False)

            else:
                return_dict["status"] = "0"
                return_dict["count"] = "0"
                return_dict["message"] = "查询异常"
                app.logger.warning("查询所有用户组：查询异常")
                return json.dumps(return_dict, ensure_ascii=False)

        else:
            return_dict["status"] = "0"
            return_dict["message"] = "传入参数错误"
            app.logger.warning("查询所有用户组：传入参数错误")
            return json.dumps(return_dict, ensure_ascii=False)

    return_dict["status"] = "0"
    return_dict["message"] = "未知错误"
    app.logger.warning("查询所有用户组：未知错误")
    return json.dumps(return_dict, ensure_ascii=False)

# 查询用户组成员
@app.route('/select_user_group',methods=['POST'])
def select_user_group():
    return_dict = {'status': '0','count': 'none', 'group':'none', 'message': 'none'}
    if request.method == "POST":
        # 验证参数是否一致
        if len(request.get_data()) != 0 and len(request.values) == 2:
            key = request.values.get("token")
            ugroup = request.values.get("group")
            # 查询UserDB表内是否存在用户传入的key
            ref_data = select_sql("select user_key from UserDB where user_key='{}';".format(key))
            if len(ref_data) != 0 and ref_data != False:
                # 定义组合模板
                object_list = []

                # 查询组并去重后放入ref
                ref_select_data = select_sql("select uname,mobile,is_auth from ObjectDB where ugroup='{}';".format(ugroup))
                if ref_select_data != False:
                    for each in ref_select_data:
                        object_list.append(each)

                    # 返回系统部门
                    return_dict["status"] = "1"
                    return_dict["count"] = len(object_list)

                    if len(object_list)==0:
                        return_dict["group"] = "none"
                    else:
                        return_dict["group"] = ugroup

                    return_dict["message"] = object_list
                    return json.dumps(return_dict, ensure_ascii=False)

                else:
                    return_dict["status"] = "0"
                    return_dict["group"] = "none"
                    return_dict["count"] = "0"
                    return_dict["message"] = "查询异常"
                    app.logger.warning("查询用户组成员：查询异常")
                    return json.dumps(return_dict, ensure_ascii=False)

            else:
                return_dict["status"] = "0"
                return_dict["group"] = "none"
                return_dict["count"] = "0"
                return_dict["message"] = "查询异常"
                app.logger.warning("查询用户组成员：查询异常")
                return json.dumps(return_dict, ensure_ascii=False)

        else:
            return_dict["status"] = "0"
            return_dict["group"] = "none"
            return_dict["count"] = "0"
            return_dict["message"] = "传入参数错误"
            app.logger.warning("查询用户组成员：传入参数错误")
            return json.dumps(return_dict, ensure_ascii=False)

    return_dict["status"] = "0"
    return_dict["group"] = "none"
    return_dict["count"] = "0"
    return_dict["message"] = "未知错误"
    app.logger.warning("查询用户组成员：未知错误")
    return json.dumps(return_dict, ensure_ascii=False)

# 修改用户组
@app.route('/update_user_group',methods=['POST'])
def update_user_group():
    return_dict = {'status': '0','message': 'none'}
    if request.method == "POST":
        # 验证参数是否一致
        if len(request.get_data()) != 0 and len(request.values) == 3:
            key = request.values.get("token")
            mobile = request.values.get("mobile")
            ugroup = request.values.get("group")
            # 查询UserDB表内是否存在用户传入的key
            ref_data = select_sql("select user_key from UserDB where user_key='{}';".format(key))
            if len(ref_data) != 0 and ref_data != False:
                # 查询是否存在传入手机号
                if len(select_sql("select mobile from ObjectDB where mobile='{}';".format(mobile))) == 1:
                    # 更新用户组
                    if update_sql("update ObjectDB set ugroup='{}' where user_key='{}' and mobile='{}';".format(ugroup,key,mobile)) != False:
                        # 返回系统部门
                        return_dict["status"] = "1"
                        return_dict["message"] = "已更新"
                        return json.dumps(return_dict, ensure_ascii=False)
                    else:
                        return_dict["status"] = "0"
                        return_dict["message"] = "查询异常"
                        app.logger.warning("修改用户组：查询异常")
                        return json.dumps(return_dict, ensure_ascii=False)

                # 否则说明传入手机号不存在,则直接退出
                else:
                    return_dict["status"] = "0"
                    return_dict["message"] = "用户组不存在,或手机号错误"
                    app.logger.warning("修改用户组：用户组不存在,或手机号错误")
                    return json.dumps(return_dict, ensure_ascii=False)
            else:
                return_dict["status"] = "0"
                return_dict["message"] = "查询异常"
                app.logger.warning("修改用户组：查询异常")
                return json.dumps(return_dict, ensure_ascii=False)

        else:
            return_dict["status"] = "0"
            return_dict["message"] = "传入参数错误"
            app.logger.warning("修改用户组：传入参数错误")
            return json.dumps(return_dict, ensure_ascii=False)

    return_dict["status"] = "0"
    return_dict["message"] = "未知错误"
    app.logger.warning("修改用户组：未知错误")
    return json.dumps(return_dict, ensure_ascii=False)

# ----------------------------------------------------------------------------------------------------------------------
# 经纬度返回相关接口
# ----------------------------------------------------------------------------------------------------------------------

# 返回经纬度函数调用
def GetLocationLatFunction(mobile):
    return_dict = {'status': '0', 'mobile': 'none', 'localtime': '0', 'longitude': 'none', 'latitude': 'none'}

    postcontent = '<?xml version="1.0" encoding="GB2312"?>'
    postcontent += '<REQ>'
    postcontent += '<CLIENT>'
    postcontent += '<LCSCLIENTID>{}</LCSCLIENTID>'.format("")
    postcontent += '<PASSWORD>{}</PASSWORD>'.format("")
    postcontent += '</CLIENT>'
    postcontent += '<ORIGINATOR>'
    postcontent += '<ORID>{}</ORID>'.format(mobile)
    postcontent += '<ORID_TYPE>2</ORID_TYPE>'
    postcontent += '</ORIGINATOR>'
    postcontent += '<SERVICEID>{}</SERVICEID>'.format("")
    postcontent += '<LIR>'
    postcontent += '<ORIGUSER_ACCESSTYPE>3</ORIGUSER_ACCESSTYPE>'
    postcontent += '<FINDME_INDIC>0</FINDME_INDIC>'
    postcontent += '<MSIDS>'
    postcontent += '<MSID>{}</MSID>'.format(mobile)
    postcontent += '<MSID_TYPE></MSID_TYPE>'
    postcontent += '</MSIDS>'
    postcontent += '<POSREQTYPE></POSREQTYPE>'
    postcontent += '<GEO_INFO>'
    postcontent += '<COORD_SYS>LL</COORD_SYS>'
    postcontent += '<DATUM></DATUM>'
    postcontent += '<LL_FORMAT></LL_FORMAT>'
    postcontent += '</GEO_INFO>'
    postcontent += '<PQOS>'
    postcontent += '<RESP_REQ></RESP_REQ>'
    postcontent += '<HOR_ACC></HOR_ACC>'
    postcontent += '<ALT_ACC></ALT_ACC>'
    postcontent += '</PQOS>'
    postcontent += '<PRIO></PRIO>'
    postcontent += '</LIR>'
    postcontent += '</REQ>'

    try:
        req = requests.get("http://127.0.0.1:7001", data=postcontent.encode('utf-8'), headers={'Content-Type': 'text/xml'})
        xmlparse = xmltodict.parse(req.text)
        jsonstr = json.loads(json.dumps(xmlparse, indent=1))

        # 返回经纬度并打包成字典格式
        if jsonstr["ANS"]["LIA"]["RESULT"] == "0":
            LOCALTIME = str(jsonstr["ANS"]["LIA"]["POSINFOS"]["POSINFO"]["LOCALTIME"])
            LATITUDE = str(jsonstr["ANS"]["LIA"]["POSINFOS"]["POSINFO"]["LATITUDE"])
            LONGITUDE = str(jsonstr["ANS"]["LIA"]["POSINFOS"]["POSINFO"]["LONGITUDE"])

            return_dict['status'] = '1'
            return_dict['mobile'] = mobile
            return_dict['localtime'] = LOCALTIME
            return_dict['longitude'] = LONGITUDE
            return_dict['latitude'] = LATITUDE

            app.logger.warning("定位成功,次数增加")
            return return_dict

        else:
            return_dict['status'] = '0'
            return_dict['mobile'] = '18265477568'
            return_dict['localtime'] = 'none'
            return_dict['longitude'] = 'none'
            return_dict['latitude'] = 'none'

            app.logger.warning("定位失败,提供手机号或格式有误")
            return return_dict

    except Exception:
        return_dict['status'] = '0'
        return_dict['mobile'] = '18265477568'
        return_dict['localtime'] = 'none'
        return_dict['longitude'] = 'none'
        return_dict['latitude'] = 'none'

        app.logger.warning("定位接口函数异常")
        return return_dict


# 调用经纬度函数
def GetLocationLatFunction(mobile):
    url = "http://127.0.0.1:9050/api/get_lat"
    response = requests.post(url,timeout=5,data={"mobile": mobile})
    get_to_json = response.json()
    return get_to_json

# 返回经纬度路由函数
@app.route('/select_lat',methods=['POST'])
def select_lat():
    return_dict = {'status': '0', 'mobile': 'none', 'localtime': '0', 'longitude': 'none', 'latitude': 'none'}

    if request.method == "POST":
        if len(request.get_data()) != 0 and len(request.values) == 2:
            key = request.values.get("token")
            mobile = request.values.get("mobile")

            # 通过说明是联通的手机号
            if mobile.strip()[0:3] in TelList or mobile.strip()[0:5] in TelList:
                # 验证是否登录
                ref_UserDB_data = select_sql("select user_key from UserDB;")
                for each in ref_UserDB_data:
                    if(each[0] == key):

                        # 判断是否为授权用户
                        select_auth = select_sql("select is_auth,uname from ObjectDB where mobile='{}'".format(mobile))
                        if select_auth[0][0] != "已授权用户":
                            return_dict = {'status': '0', 'message': '未授权用户,请授权'}
                            return json.dumps(return_dict, ensure_ascii=False)
                        else:
                            # 如果授权了,直接调用定位函数
                            return_dict = GetLocationLatFunction(mobile)

                            # LocationCountDB 中的定位次数递增一次
                            ref_LocationCount = select_sql("select lat_count from LocationCountDB where mobile='{}';".format(mobile))
                            if ref_LocationCount != False:
                                new_count = int(ref_LocationCount[0][0]) + 1
                                update_sql("update LocationCountDB set lat_count={} where mobile='{}'".format(new_count,mobile))

                            return json.dumps(return_dict, ensure_ascii=False)
            else:
                app.logger.warning("返回经纬度：请输入联通手机号")
                return_dict = {'status': '0', 'message': '请输入联通手机号'}
                return json.dumps(return_dict, ensure_ascii=False)
        else:
            app.logger.warning("返回经纬度：传入参数错误")
            return_dict = {'status': '0','message': '传入参数错误'}
            return json.dumps(return_dict, ensure_ascii=False)

    return json.dumps(return_dict, ensure_ascii=False)

# 查询总计调用次数与费率信息
@app.route('/select_all_count',methods=['POST'])
def select_all_count():
    return_dict = {'status': '0', 'lat_count': '0', 'lat_rate':'0.00', 'trajectory_count': '0', 'trajectory_rate':'0.00', 'enclosure_count':'0', 'enclosure_rate':'0.0'}

    if request.method == "POST":
        if len(request.get_data()) != 0 and len(request.values) == 1:
            key = request.values.get("token")

            # 验证是否登录
            ref_UserDB_data = select_sql("select user_key from UserDB;")
            for each in ref_UserDB_data:
                if (each[0] == key):

                    # 查询统计次数
                    ref_data = select_sql("select lat_count,lat_rate,trajectory_count,trajectory_rate,enclosure_count,enclosure_rate"
                                          " from LocationCountDB;")

                    lat_count = 0
                    trajectory_count = 0
                    enclosure_count = 0

                    # 累加计数器
                    for item in ref_data:
                        lat_count = lat_count + int(item[0])
                        trajectory_count = trajectory_count + int(item[2])
                        enclosure_count = enclosure_count + int(item[4])

                    return_dict['status'] = '1'
                    return_dict['lat_count'] = lat_count
                    return_dict['lat_rate'] = item[1]
                    return_dict['trajectory_count'] = trajectory_count
                    return_dict['trajectory_rate'] = item[3]
                    return_dict['enclosure_count'] = enclosure_count
                    return_dict['enclosure_rate'] = item[5]
                    return json.dumps(return_dict, ensure_ascii=False)

        else:
            app.logger.warning("查询总计调用次数与费率信息：传入参数错误")
            return_dict = {'status': '0','message': '传入参数错误'}
            return json.dumps(return_dict, ensure_ascii=False)

    app.logger.warning("查询总计调用次数与费率信息：未知错误")
    return_dict = {'status': '0', 'message': '未知错误'}
    return json.dumps(return_dict, ensure_ascii=False)

# 查询某手机号调用次数与费率
@app.route('/select_mobile_count',methods=['POST'])
def select_mobile_count():
    return_dict = {'status': '0', 'mobile': 'none', 'lat_count': '0', 'lat_rate':'0.00', 'trajectory_count': '0', 'trajectory_rate':'0.00', 'enclosure_count':'0', 'enclosure_rate':'0.0'}

    if request.method == "POST":
        if len(request.get_data()) != 0 and len(request.values) == 2:
            key = request.values.get("token")
            mobile = request.values.get("mobile")

            # 通过说明是联通的手机号
            if mobile.strip()[0:3] in TelList or mobile.strip()[0:5] in TelList:
                # 验证是否登录
                ref_UserDB_data = select_sql("select user_key from UserDB;")
                for each in ref_UserDB_data:
                    if (each[0] == key):

                        # 查询统计次数
                        ref_data = select_sql(
                            "select mobile,lat_count,lat_rate,trajectory_count,trajectory_rate,enclosure_count,enclosure_rate"
                            " from LocationCountDB where mobile='{}';".format(mobile))

                        return_dict['status'] = '1'
                        return_dict['mobile'] = ref_data[0][0]
                        return_dict['lat_count'] = ref_data[0][1]
                        return_dict['lat_rate'] = ref_data[0][2]
                        return_dict['trajectory_count'] = ref_data[0][3]
                        return_dict['trajectory_rate'] = ref_data[0][4]
                        return_dict['enclosure_count'] = ref_data[0][5]
                        return_dict['enclosure_rate'] = ref_data[0][6]

                        return json.dumps(return_dict, ensure_ascii=False)

            else:
                app.logger.warning("查询某手机号调用次数与费率：请输入联通手机号")
                return_dict = {'status': '0', 'message': '请输入联通手机号'}
                return json.dumps(return_dict, ensure_ascii=False)

        else:
            app.logger.warning("查询某手机号调用次数与费率：传入参数错误")
            return_dict = {'status': '0', 'message': '传入参数错误'}
            return json.dumps(return_dict, ensure_ascii=False)

    app.logger.warning("查询某手机号调用次数与费率：未知错误")
    return_dict = {'status': '0', 'message': '未知错误'}
    return json.dumps(return_dict, ensure_ascii=False)

# ----------------------------------------------------------------------------------------------------------------------
# 鉴权接口 相关接口
# ----------------------------------------------------------------------------------------------------------------------

# 调用发送短信
def Send_Msg(mobile,msg):
    url = "http://127.0.0.1:9050/api/send_message"
    response = requests.post(url,timeout=5,data={"mobile": mobile,"message": msg})
    get_to_json = response.json()
    return get_to_json


# 查询用户权限状态
@app.route('/select_auth_table',methods=['POST'])
def select_auth_table():
    return_dict = {'status': '0','unauthorized': [],'authorized': []}

    if request.method == "POST":
        if len(request.get_data()) != 0 and len(request.values) == 1:
            key = request.values.get("token")

            # 验证是否登录
            ref_UserDB_data = select_sql("select user_key from UserDB;")
            for each in ref_UserDB_data:
                if (each[0] == key):
                    # 查询统计次数
                    ref_data = select_sql("select mobile,is_auth from ObjectDB;")

                    not_auth = []
                    success_auth = []

                    for each in ref_data:
                        if each[1] == "未授权用户":
                            not_auth.append(each[0])
                        elif each[1] == "已授权用户":
                            success_auth.append(each[0])

                    return_dict['status'] = '1'
                    return_dict['unauthorized'] = not_auth
                    return_dict['authorized'] = success_auth
                    return json.dumps(return_dict, ensure_ascii=False)
        else:
            app.logger.warning("查询用户权限状态：传入参数错误")
            return_dict = {'status': '0', 'message': '传入参数错误'}
            return json.dumps(return_dict, ensure_ascii=False)

    app.logger.warning("查询用户权限状态：未知错误")
    return_dict = {'status': '0', 'message': '未知错误'}
    return json.dumps(return_dict, ensure_ascii=False)

# 发送验证码
@app.route('/send_message',methods=['POST'])
def send_message():
    return_dict = {'status': '0' ,'message':'none'}

    if request.method == "POST":
        if len(request.get_data()) != 0 and len(request.values) == 2:
            key = request.values.get("token")
            mobile = request.values.get("mobile")

            # 验证是否登录
            ref_UserDB_data = select_sql("select user_key from UserDB;")
            for each in ref_UserDB_data:
                if (each[0] == key):

                    # 查询是否授权
                    ref_data = select_sql("select mobile,is_auth from ObjectDB;")
                    for each in ref_data:

                        # 如果是未授权则提供验证
                        if each[1] == "未授权用户" and each[0] == mobile:
                            msg_code = generate_random_str(6)

                            # 设置五分钟时间戳
                            timeStamp = int(time.time()) + 300
                            dateArray = datetime.datetime.fromtimestamp(timeStamp)
                            otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")

                            # 判断是插入数据还是更新
                            select_flag = select_sql("select mobile from VerificationCodeDB where mobile='{}'".format(mobile))

                            if len(select_flag) == 0:
                                insert_sql("insert into VerificationCodeDB(mobile,code,time_stamp) values('{}','{}',{})".format(mobile,msg_code,timeStamp))
                                message_code = "您本次登录的验证码是：{}，有效时间：5分钟。验证码有效期至：{}".format(str(msg_code), otherStyleTime)
                                Send_Msg(mobile, message_code)
                                print(message_code)
                            else:
                                update_sql("update VerificationCodeDB set code='{}',time_stamp='{}' where mobile='{}'".format(msg_code,timeStamp,mobile))
                                message_code = "刷新验证码是：{}，有效时间：5分钟。验证码有效期至：{}".format(str(msg_code), otherStyleTime)
                                print(message_code)
                                Send_Msg(mobile,message_code)

                            app.logger.warning("发送验证码：验证码已发送，请注意查收")
                            return_dict = {'status': '1', 'message': '验证码已发送,请注意查收'}
                            return json.dumps(return_dict, ensure_ascii=False)
        else:
            app.logger.warning("发送验证码：传入参数错误")
            return_dict = {'status': '0', 'message': '传入参数错误'}
            return json.dumps(return_dict, ensure_ascii=False)

    app.logger.warning("发送验证码：未知错误")
    return_dict = {'status': '0', 'message': '未知错误'}
    return json.dumps(return_dict, ensure_ascii=False)

# 授权接口
@app.route('/set_auth',methods=['POST'])
def set_auth():
    return_dict = {'status': '0','mobile':'none','message':'none'}

    if request.method == "POST":
        if len(request.get_data()) != 0 and len(request.values) == 4:
            key = request.values.get("token")
            mobile = request.values.get("mobile")
            vf_code = request.values.get("code")
            flag = request.values.get("flag")

            if flag == "False":
                app.logger.warning("授权接口：如需要授权，请接受许可协议")
                return_dict = {'status': '0', 'message': '如需授权,请接受许可协议'}
                return json.dumps(return_dict, ensure_ascii=False)

            elif flag == "True":
                # 验证是否登录
                ref_UserDB_data = select_sql("select user_key from UserDB;")
                for each in ref_UserDB_data:
                    if (each[0] == key):

                        # 查询授权记录
                        ref_data = select_sql("select is_auth from ObjectDB where mobile='{}';".format(mobile))

                        # 如果是未授权则继续
                        if ref_data[0][0] == "未授权用户":
                            LocaltimeStamp = int(time.time())
                            try:
                                # 查询当前用户验证码与时间戳
                                ref_vfa = select_sql("select mobile,time_stamp from VerificationCodeDB where mobile='{}';".format(mobile))
                                if ref_vfa != False:

                                    # 验证时间戳是否有效
                                    if LocaltimeStamp <= ref_vfa[0][1]:

                                        # 检查用户输入验证码是否有效,如果有效则将该用户设置为已授权用户.
                                        ref_vf_code = select_sql("select code from VerificationCodeDB where mobile='{}'".format(mobile))

                                        # 验证码正确
                                        if ref_vf_code[0][0] == vf_code:

                                            update_sql("update ObjectDB set is_auth='{}' where mobile='{}'".format("已授权用户",mobile))

                                            return_dict = {'status': '1', 'message': '授权完成'}
                                            return json.dumps(return_dict, ensure_ascii=False)

                                        # 验证码错误
                                        else:
                                            app.logger.warning("授权接口：验证码错误")
                                            return_dict = {'status': '1', 'message': '验证码错误,授权失败'}
                                            return json.dumps(return_dict, ensure_ascii=False)


                                    elif LocaltimeStamp > ref_vfa[0][1]:
                                        delete_sql("delete from VerificationCodeDB where mobile='{}'".format(mobile))
                                        app.logger.warning("授权接口：验证码已过期，请重新获取")
                                        return_dict = {'status': '0', 'message': '验证码已过期,请重新获取验证码'}
                                        return json.dumps(return_dict, ensure_ascii=False)

                            except Exception:
                                app.logger.warning("授权接口：请发送验证码，然后在调用该接口，完成授权")
                                return_dict = {'status': '0', 'message': '请先发送验证码,然后在调用该接口,完成授权'}
                                return json.dumps(return_dict, ensure_ascii=False)
                        else:
                            # 如果已授权过,删除表中的验证码字段
                            delete_sql("delete from VerificationCodeDB where mobile='{}'".format(mobile))
                            app.logger.warning("授权接口：用户已授权，无需继续授权")
                            return_dict = {'status': '0', 'message': '用户已授权,无需继续授权'}
                            return json.dumps(return_dict, ensure_ascii=False)
        else:
            app.logger.warning("授权接口：传入参数错误")
            return_dict = {'status': '0', 'message': '传入参数错误'}
            return json.dumps(return_dict, ensure_ascii=False)

    app.logger.warning("授权接口：未知错误")
    return_dict = {'status': '0', 'message': '未知错误'}
    return json.dumps(return_dict, ensure_ascii=False)

# 取消授权接口
@app.route('/unset_auth',methods=['POST'])
def unset_auth():

    return_dict = {'status': '0','mobile':'none','message':'none'}

    if request.method == "POST":
        if len(request.get_data()) != 0 and len(request.values) == 2:
            key = request.values.get("token")
            mobile = request.values.get("mobile")

            # 验证是否登录
            ref_UserDB_data = select_sql("select user_key from UserDB;")

            if ref_UserDB_data != False:
                for each in ref_UserDB_data:
                    if (each[0] == key):
                        # 查询授权记录
                        ref_data = select_sql("select is_auth from ObjectDB where mobile='{}';".format(mobile))

                        # 未授权直接返回
                        if ref_data[0][0] == "未授权用户":
                            return_dict['status'] = '0'
                            return_dict['mobile'] = mobile
                            return_dict['message'] = '未授权用户,无需取消授权'

                            app.logger.warning("取消授权: 未授权用户,无需取消授权")
                            return json.dumps(return_dict, ensure_ascii=False)

                        # 已授权直接改为未授权
                        else:
                            if update_sql("update ObjectDB set is_auth='{}' where mobile='{}'".format("未授权用户",mobile)) != False:
                                return_dict['status'] = '1'
                                return_dict['mobile'] = mobile
                                return_dict['message'] = '取消授权成功'
                                app.logger.warning("取消授权：取消授权成功")
                                return json.dumps(return_dict, ensure_ascii=False)
        else:
            app.logger.warning("取消授权：传入参数错误")
            return_dict = {'status': '0', 'message': '传入参数错误'}
            return json.dumps(return_dict, ensure_ascii=False)

    app.logger.warning("取消授权：未知错误")
    return_dict = {'status': '0', 'message': '未知错误'}
    return json.dumps(return_dict, ensure_ascii=False)


# ----------------------------------------------------------------------------------------------------------------------
# 轨迹任务
# ----------------------------------------------------------------------------------------------------------------------

# 创建轨迹任务列表
@app.route('/create_trajectory_task',methods=['POST'])
def create_trajectory_task():

    return_dict = {'status': '0','mobile':'none','message':'none'}

    if request.method == "POST":
        if len(request.get_data()) != 0 and len(request.values) == 6:
            key = request.values.get("token")
            uid = request.values.get("uid")
            task_name = request.values.get("task_name")
            mobile = request.values.get("mobile")
            start_time = request.values.get("start_time")
            end_time = request.values.get("end_time")

            # 验证是否登录
            ref_UserDB_data = select_sql("select user_key from UserDB;")

            if ref_UserDB_data != False:
                for each in ref_UserDB_data:
                    if (each[0] == key):
                        # 查询授权记录
                        ref_data = select_sql("select is_auth from ObjectDB where mobile='{}';".format(mobile))

                        # 未授权直接返回
                        if ref_data[0][0] == "未授权用户":
                            return_dict['status'] = '0'
                            return_dict['mobile'] = mobile
                            return_dict['message'] = '未授权用户,请授权后在创建任务'

                            app.logger.warning("轨迹任务：未授权用户,请授权后在创建任务")
                            return json.dumps(return_dict, ensure_ascii=False)

                        # 已授权用户直接插入一条记录
                        else:
                            if insert_sql("insert into TrajectoryTaskDB(uid,task_name,mobile,start_time,end_time,count,rate) values('{}','{}',{},'{}','{}','0','0')".format(uid,task_name,mobile,start_time,end_time)) != False:
                                return_dict['status'] = '1'
                                return_dict['mobile'] = mobile
                                return_dict['message'] = '创建轨迹任务成功'
                                app.logger.warning("轨迹任务：创建轨迹任务成功")
                                return json.dumps(return_dict, ensure_ascii=False)
        else:
            app.logger.warning("轨迹任务：传入参数错误")
            return_dict = {'status': '0', 'message': '传入参数错误'}
            return json.dumps(return_dict, ensure_ascii=False)

    app.logger.warning("轨迹任务：未知错误")
    return_dict = {'status': '0', 'message': '未知错误'}
    return json.dumps(return_dict, ensure_ascii=False)

# 输出当前所有轨迹任务
@app.route('/select_trajectory_task',methods=['POST'])
def select_trajectory_task():
    return_dict = {'status': '0','count':'0', 'message':'none'}

    if request.method == "POST":
        if len(request.get_data()) != 0 and len(request.values) == 1:
            key = request.values.get("token")

            # 验证是否登录
            ref_UserDB_data = select_sql("select user_key from UserDB;")

            if ref_UserDB_data != False:
                for each in ref_UserDB_data:
                    if (each[0] == key):

                        ref_list = []

                        # 查询所有轨迹任务
                        ref_data = select_sql("select * from TrajectoryTaskDB;")

                        # 拼接字典
                        for item in ref_data:
                            ref_dict = {"uid": "0", "task_name": "none","mobile":"none","start_time":"none","end_time":"none","count":"0","rate":"0"}
                            ref_dict["uid"] = item[0]
                            ref_dict["task_name"] = item[1]
                            ref_dict["mobile"] = item[2]
                            ref_dict["start_time"] = item[3]
                            ref_dict["end_time"] = item[4]
                            ref_dict["count"] = item[5]
                            ref_dict["rate"] = item[6]
                            ref_list.append(ref_dict)

                        return_dict["status"] = "1"
                        return_dict["count"] = len(ref_list)
                        return_dict["message"] = ref_list
                        return json.dumps(return_dict, ensure_ascii=False)
        else:
            app.logger.warning("轨迹任务：传入参数错误")
            return_dict = {'status': '0', 'message': '传入参数错误'}
            return json.dumps(return_dict, ensure_ascii=False)

    app.logger.warning("轨迹任务：未知错误")
    return_dict = {'status': '0', 'message': '未知错误'}
    return json.dumps(return_dict, ensure_ascii=False)

# 删除一个轨迹任务
@app.route('/delete_trajectory_task',methods=['POST'])
def delete_trajectory_task():
    return_dict = {'status': '0','message':'none'}

    if request.method == "POST":
        if len(request.get_data()) != 0 and len(request.values) == 2:
            key = request.values.get("token")
            uid = request.values.get("uid")

            # 验证是否登录
            ref_UserDB_data = select_sql("select user_key from UserDB;")

            if ref_UserDB_data != False:
                for each in ref_UserDB_data:
                    if (each[0] == key):

                        # 删除某一个轨迹任务
                        ref = delete_sql("delete from TrajectoryTaskDB where uid = '{}'".format(uid))

                        if ref == True:
                            return_dict["status"] = "1"
                            return_dict["message"] = "删除成功"
                            return json.dumps(return_dict, ensure_ascii=False)
                        else:
                            return_dict["status"] = "0"
                            return_dict["message"] = "删除失败"
                            return json.dumps(return_dict, ensure_ascii=False)

                        return_dict["status"] = "0"
                        return_dict["message"] = "用户登录异常"
                        return json.dumps(return_dict, ensure_ascii=False)
        else:
            app.logger.warning("轨迹任务：传入参数错误")
            return_dict = {'status': '0', 'message': '传入参数错误'}
            return json.dumps(return_dict, ensure_ascii=False)

    app.logger.warning("轨迹任务：未知错误")
    return_dict = {'status': '0', 'message': '未知错误'}
    return json.dumps(return_dict, ensure_ascii=False)

# 查询轨迹任务历史
@app.route('/select_trajectory_task_history',methods=['POST'])
def select_trajectory_task_history():
    return_dict = {'status': '0','message':'none'}

    if request.method == "POST":
        if len(request.get_data()) != 0 and len(request.values) == 4:
            key = request.values.get("token")
            mobile = request.values.get("mobile")
            s_time = request.values.get("start_time")
            e_time = request.values.get("end_time")

            # 验证是否登录
            ref_UserDB_data = select_sql("select user_key from UserDB;")

            if ref_UserDB_data != False:
                for each in ref_UserDB_data:
                    if (each[0] == key):
                        ref_his = []
                        # 查询轨迹任务
                        select_task_his = select_sql("select local_time,x,y from TrajectoryHistoryTableDB where mobile='{}' and local_time >= '{}' and local_time <= '{}'".format(mobile,s_time,e_time))
                        if select_task_his != None or select_task_his != []:
                            for each in select_task_his:
                                task_his = []
                                task_his.append(each[0])
                                task_his.append(each[1])
                                task_his.append(each[2])
                                ref_his.append(task_his)

                        print(ref_his)
                        return_dict["status"] = "1"
                        return_dict["message"] = ref_his
                        return json.dumps(return_dict, ensure_ascii=False)
        else:
            app.logger.warning("轨迹任务：传入参数错误")
            return_dict = {'status': '0', 'message': '传入参数错误'}
            return json.dumps(return_dict, ensure_ascii=False)

    app.logger.warning("轨迹任务：未知错误")
    return_dict = {'status': '0', 'message': '未知错误'}
    return json.dumps(return_dict, ensure_ascii=False)

# 用于定时巡检,检查是否需要定位
def MyThread():
    while True:
        select_value = select_sql("select * from TrajectoryTaskDB;")

        # 如果查询到结果
        if select_value != None or select_value != []:

            for each in select_value:
                time.sleep(2)
                timeStamp = int(time.time())
                dateArray = datetime.datetime.fromtimestamp(timeStamp)
                otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M")

                start_timeStamp = int(time.mktime(time.strptime(each[3], "%Y-%m-%d %H:%M")))
                end_timeStamp = int(time.mktime(time.strptime(each[4], "%Y-%m-%d %H:%M")))

                # 判断是否在某个区间
                if timeStamp >= start_timeStamp and timeStamp <= end_timeStamp:
                    insert_sql("insert into TrajectoryHistoryTableDB(mobile,start_time,end_time,local_time,x,y) values('{}','{}','{}','{}',{},{})".format(each[2],each[3],each[4],otherStyleTime, 12.5,22.4))
        time.sleep(900)

# ----------------------------------------------------------------------------------------------------------------------
# 其他功能
# ----------------------------------------------------------------------------------------------------------------------

@app.route('/get_version',methods=['POST'])
def get_version():
    return_dict = {'status': '1','version': '1.0.0', 'build': '2022-04-06 9:57'}
    return json.dumps(return_dict, ensure_ascii=False)

@app.errorhandler(404)
def not_found(error):
    return_dict = {'status': '404', 'message': '404'}
    return json.dumps(return_dict, ensure_ascii=False)

@app.errorhandler(405)
def not_found(error):
    return_dict = {'status': '405', 'message': '405'}
    return json.dumps(return_dict, ensure_ascii=False)

@app.errorhandler(500)
def not_found(error):
    return_dict = {'status': '500', 'message': '500'}
    return json.dumps(return_dict, ensure_ascii=False)

@app.errorhandler(400)
def not_found(error):

    return_dict = {'status': '400', 'message': 'Bad Request'}
    return json.dumps(return_dict, ensure_ascii=False)

@app.errorhandler(409)
def not_found(error):
    return_dict = {'status': '409', 'message': 'Conflict'}
    return json.dumps(return_dict, ensure_ascii=False)

if __name__ == '__main__':
    #thread = threading.Thread(target=MyThread)
    #thread.start()
    # app.run(host='127.0.0.1',port='9050',debug=False)
    app.run(host='127.0.0.1', port='80', debug=False)
    #app.run(port=80,debug=False)
