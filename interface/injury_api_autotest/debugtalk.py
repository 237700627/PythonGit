import datetime
import time
import os
import requests

from config import url
import random
import pymysql

def base_url():
    default_request = {
        'base_url': url,
        'headers': {
            "Content-Type": "application/json;charset=UTF-8"}
    }

    return default_request['base_url']

# 生成一个指定长度的随机数
def random_Num(length, string=[]):
    for i in range(length):
            y = str(random.randint(0, 9))
            string.append(y)
    string = ''.join(string)
    return string

# a = random_Num(9, ['1','3'])
# b = random_Num(6, ['粤','B'])
# c = random_Num(9)
# print(a,b,c)

def time_to_timestamp(str_time):
    '''
    str_time格式：%Y-%m-%d，如2019-04-02
    将时间转换为时间戳
    1.字符时间先转换为时间数组
    2.将时间数组转换为时间戳
    '''
    str_time_all=str_time+" 00:00:00"
    time_array=time.strptime(str_time_all,"%Y-%m-%d %H:%M:%S")
    time_stamp=int(time.mktime(time_array)*1000) #接口的时间戳单位是毫秒
    return time_stamp


temp=time_to_timestamp("2019-05-14")
print(temp)



# # 连接数据库公用方法（dev）
# def query_mysql(sql, *params, database="zbcf_injury"):
#     conn = pymysql.connect(host="rm-wz97oujls3998784i.mysql.rds.aliyuncs.com", user="appuser",
#                            password="tmp-PW4root@2018", database=database, charset='utf8',
#                            cursorclass=pymysql.cursors.DictCursor)
#     cursor = conn.cursor()
#     cursor.execute(sql, params)
#     data = cursor.fetchone()
#     cursor.close()
#     conn.close()
#     return data



# 连接数据库公用方法（test）
def query_mysql(sql, *params, database="zbcf_injury_test"):
    conn = pymysql.connect(host="rm-wz97oujls3998784i.mysql.rds.aliyuncs.com", user="testuser",
                           password="testuser@2018", database=database, charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    cursor.execute(sql, params)
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return data

#成功登录获取token，拼接到headers中
def setup_hook_token(request):
    #print(request)
    url_path="http://testrenshang.cias.cn/injury/user/pc/login"
    header={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    payload={"loginName":"xiao2qiu","loginPass":"Y2lhczEyMzQ1Ng==","verifyCode":"tubd"}
    req=requests.post(url=url_path,headers=header,params=payload).json()
    token=req['data']['token']
    request["headers"]['token']=token
    #print(token)
    #print(request)

def setup_hook_notoken(request):
    token=""
    request["headers"]['token']=token


# 模拟订单超过48/12小时/7天(dev)
# 只需将数据库登录码的过期时间设置为当前时间
def orderTimeOut(order_id, database="zbcf_injury"):
    conn = pymysql.connect(host="rm-wz97oujls3998784i.mysql.rds.aliyuncs.com", user="appuser",
                           password="tmp-PW4root@2018", database=database, charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    now = datetime.datetime.now()
    now = now.strftime('%Y-%m-%d %H:%M:%S')
    sql = "UPDATE t_auth_info t SET end_effect_time = '%s' WHERE t.operation_id = (SELECT id from t_operation where  order_id = '%s')" % (now, order_id)
    effectRows = cursor.execute(sql)
    conn.commit()
    #print('make order time out!')
    cursor.close()
    conn.close()
    return effectRows

# 模拟订单超过48/12小时/7天(test)
# 只需将数据库登录码的过期时间设置为当前时间
def orderTimeOut(order_id, database="zbcf_injury_test"):
    conn = pymysql.connect(host="rm-wz97oujls3998784i.mysql.rds.aliyuncs.com", user="testuser",
                           password="testuser@2018", database=database, charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    now = datetime.datetime.now()
    now = now.strftime('%Y-%m-%d %H:%M:%S')
    sql = "UPDATE t_auth_info t SET end_effect_time = '%s' WHERE t.operation_id = (SELECT id from t_operation where  order_id = '%s')" % (now, order_id)
    effectRows = cursor.execute(sql)
    conn.commit()
    #print('make order time out!')
    cursor.close()
    conn.close()
    return effectRows

# # 将订单表t_order的update_time时间设置为48/12小时前的时间，默认为48小时(172800S)(dev)
# def orderUpdate48h(order_id,time_ago=172800,database="zbcf_injury"):
#     conn = pymysql.connect(host="rm-wz97oujls3998784i.mysql.rds.aliyuncs.com", user="appuser",
#                            password="tmp-PW4root@2018", database=database, charset='utf8',
#                            cursorclass=pymysql.cursors.DictCursor)
#     cursor = conn.cursor()
#     #获取当前时间戳
#     now_stamp=time.time()
#     now_48hBefore_stamp=now_stamp-time_ago
#
#     #struct_time时间
#     now_struct=time.localtime(now_stamp)
#     now_5sbefore_struct=time.localtime(now_48hBefore_stamp)
#     #str格式的时间
#     now_str=time.strftime('%Y-%m-%d %H:%M:%S', now_struct)
#     now_48hBefore_stamp_str=time.strftime('%Y-%m-%d %H:%M:%S', now_5sbefore_struct)
#     # print("当前的时间：",now_str)
#     # print("48小时前的时间：",now_5sbefore_struct)
#
#     sql = "UPDATE t_order t SET update_time = '%s' WHERE id = '%s'" % (now_48hBefore_stamp_str, order_id)
#     print(sql)
#     effectRows = cursor.execute(sql)
#     conn.commit()
#     #print('The order update time was revised to 48 hours ago!')
#     cursor.close()
#     conn.close()
#     return effectRows
## orderUpdate48h('674',86400)


# 将订单表t_order的update_time时间设置为48/12小时前的时间，默认为48小时(172800S)(test)
def orderUpdate48h(order_id,time_ago=172800,database="zbcf_injury_test"):
    conn = pymysql.connect(host="rm-wz97oujls3998784i.mysql.rds.aliyuncs.com", user="testuser",
                           password="testuser@2018", database=database, charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    #获取当前时间戳
    now_stamp=time.time()
    now_48hBefore_stamp=now_stamp-time_ago

    #struct_time时间
    now_struct=time.localtime(now_stamp)
    now_5sbefore_struct=time.localtime(now_48hBefore_stamp)
    #str格式的时间
    now_str=time.strftime('%Y-%m-%d %H:%M:%S', now_struct)
    now_48hBefore_stamp_str=time.strftime('%Y-%m-%d %H:%M:%S', now_5sbefore_struct)
    # print("当前的时间：",now_str)
    # print("48小时前的时间：",now_5sbefore_struct)

    sql = "UPDATE t_order t SET update_time = '%s' WHERE id = '%s'" % (now_48hBefore_stamp_str, order_id)
    print(sql)
    effectRows = cursor.execute(sql)
    conn.commit()
    #print('The order update time was revised to 48 hours ago!')
    cursor.close()
    conn.close()
    return effectRows
#orderUpdate48h('674',86400)



def sleep(num,sleep_dec="脚本等待中..."):
    print(sleep_dec)
    time.sleep(num)

# 依据order_Id查询登录码
def queryLoginNum(orderId,del_flag='0'):
    sql = "SELECT token from t_auth_info t where t.operation_id = (SELECT id from t_operation where  order_id = '%s') and t.del_flag = '%s' order by create_time desc limit 1" %(orderId,del_flag)
    query_result = query_mysql(sql)
    return query_result['token']

# a = queryLoginNum(418)
# print (a)


# 依据operation_Id查询登录码
def opetationId_queryLoginNum(operation_Id):
    sql = "SELECT token from t_auth_info where operation_id =  '%s' and del_flag = '0'"
    query_result = query_mysql(sql, operation_Id)
    return query_result['token']

# a = queryLoginNum(290)
# print (a)


# 返回orderId，opertorId的方法
def getOrderId(order_status):
    select_orderId="select id from t_order where creator=77 and order_status='%s' order by order_no desc limit 1" %(order_status)
    data=query_mysql(select_orderId)
    print("order_id:",data["id"])
    print(type(data["id"]))
    return data["id"]
# getOrderId('05')

# 返回orderId，opertorId的方法
def getOperatorId(order_id):
    select_order_opertor="select id as opertor_id from t_operation where order_id='%s'  " %(order_id)
    #print(select_order_opertor)
    data=query_mysql(select_order_opertor)
    print("opertor_id:",data["opertor_id"])
    return data["opertor_id"]
#getOperatorId('275')

# 查询订单状态
def queryOrderStatus():
    pass


# 登录H5端获取token
def getH5Token(accessCode):
    url = "http://testrsapp.cias.cn/injury/user/h5/login"
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    data = {"accessCode": accessCode}
    req = requests.post(url=url, headers=headers, data=data).json()
    return req['data']['token']

# a = getH5Token('31583310')
# print(a)

# 登录Web端获取token
def getWebToken(accessCode):
    url = "http://testrsapp.cias.cn/injury/user/pc/login"
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    data = {"loginName": "xiao2qiu", "loginPass": "Y2lhczEyMzQ1Ng==", "verifyCode": "tubd"}
    req = requests.post(url=url, headers=headers, data=data).json()
    return req['data']['token']

# a = getWebToken('31583310')
# print(a)

# 读取文件内容
def get_file(filePath):
    return open(filePath, "rb")


# int类型转换为string
def toString(value):
    print(value, type(value))
    return str(value)
