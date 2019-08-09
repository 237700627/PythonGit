import datetime
import time

import requests

from config import url
from data import DistrictList
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

# 生成一个身份证号码，以及对应的生日
def generator():
    # 生成身份证号码
    districtcode = DistrictList[random.randint(0, len(DistrictList) - 1)]['code']
    # date = datetime.date.today() - datetime.timedelta(weeks=random.randint(1, 3840))
    date = datetime.datetime.now() - datetime.timedelta(weeks=random.randint(1, 2350))
    birthDay = date.strftime('%Y%m%d')
    randomNum = str(random.randint(100, 300))
    idnum = districtcode + birthDay + randomNum
    i = 0
    count = 0
    weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    checkcode = {'0': '1', '1': '0', '2': 'X', '3': '9', '4': '8', '5': '7', '6': '6', '7': '5', '8': '5', '9': '3', '10': '2'}
    for i in range(0, len(idnum)):
        count = count + int(idnum[i]) * weight[i]
    id = idnum + checkcode[str(count%11)]
    # 生成生日时间戳
    # timstamp = date.strftime('%Y%m%d%H%M%S')
    # timstamp = datetime.datetime.strptime(date, '%Y%m%d%H%M%S').timestamp()
    timstamp = int(time.mktime(date.timetuple()) * 1000)
    return id, timstamp

a = generator()

def returnId():
    return a[0]

def returnTimestamp():
    return a[1]



# 连接数据库公用方法
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


# 模拟订单超过48/12小时/7天
# 只需将数据库过期时间设置为当前时间
# def orderTimeOut(operation_id):
#     now = datetime.datetime.now()
#     now = now.strftime('%Y-%m-%d %H:%M:%S')
#     # delta = datetime.timedelta(days=outTime)
#     # now = now + delta
#     print(now)
#     # sql = "UPDATE t_auth_info t SET end_effect_time = str_to_date(\'%s\','%%Y-%%m-%%d %%H:%%i:%%s') WHERE t.operation_id = '%s'"
#     sql = "UPDATE t_auth_info t SET end_effect_time = '%s' WHERE t.operation_id = '%s'"
#     params = [now, operation_id]
#     update_result = query_mysql(sql, *params)
#     return update_result
#     # return now.strftime('%Y-%m-%d %H:%M:%S')
# #  有什么问题？？
# a = orderTimeOut(289)
# print(a)

# 模拟订单超过48/12小时/7天
# 只需将数据库过期时间设置为当前时间
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
    print('make order time out!')
    cursor.close()
    conn.close()
    return effectRows
# a = orderTimeOut(260)
# print(a)
def sleep(num):
    time.sleep(num)

# 依据order_Id查询登录码
def queryLoginNum(orderId):
    sql = "SELECT token from t_auth_info t where t.operation_id = (SELECT id from t_operation where  order_id = '%s') and t.del_flag = '0'"
    query_result = query_mysql(sql, orderId)
    print(orderId)
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


# 返回orderId的方法
def queryOrderId():
    pass


# 返回operationId的方法
def queryOperationId():
    pass

# 查询订单状态
def queryOrderStatus():
    pass


# # 登录PC端获取token，拼接到headers中
# def setup_hook_token(request):
#     #print(request)
#     url_path="http://testrenshang.cias.cn/injury/user/pc/login"
#     header={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
#     payload={"loginName": "haadmin003", "loginPass": "Y2lhczEyMzQ1Ng==", "verifyCode": "tubd"}
#     req=requests.post(url=url_path, headers=header, params=payload).json()
#     token=req['data']['token']
#     request["headers"]['token']=token
# #     print(token,'\n', req)
# #     print(request)
# # request = {'headers':{'Content-Type': 'application/json;charset=UTF-8', 'method': 'GET', 'url': '$uri', 'token': '$token'}}
# # setup_hook_token(request)

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
    data = {"loginName": "haadmin003", "loginPass": "Y2lhczEyMzQ1Ng==", "verifyCode": "tubd"}
    req = requests.post(url=url, headers=headers, data=data).json()
    return req['data']['token']

# a = getWebToken('31583310')
# print(a)


#