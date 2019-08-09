#!/usr/bin/python
# coding:utf-8
import base64
import hashlib
import hmac
import time
import random
import requests

from utils.Loaddata import *
from utils.mysql_operate import MySqlOperate
from utils.redishadle import RedisHandle


def loaddata(filname):
    data = Loaddata.Loadjsondata(filname)
    return data


# 获取配置文件配置
def get_config(key):
    value = os.environ.get(key)
    return value


# 生成报案号：report_no
def get_report_no():
    report_no = "AutoTESTZC" + time.strftime('%Y%m%d%H%M%S')+ str(random.randint(0,99))
    return report_no


# 生成随机车牌号
def get_car_no():
    car_no = "粤B" + time.strftime('%H%M%S')
    return car_no


# 获取系统当前时间戳，int类型
def get_current_time():
    current_time = str(int(round(time.time())))
    return current_time


# 获取系统当前时间：yyyy-MM-dd HH:mm:ss
def get_local_time_format():
    local_time_format = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(local_time_format)
    return local_time_format


# 休眠时间
def sleep_time(second_time):
    return time.sleep(second_time)


# 派单后判断是否接单
def is_order_taked(report_no):
    sleep_second = 15
    for i in range(sleep_second):
        status = get_order_status(report_no)
        if status == '04':
            return print("接单成功！")
        sleep_time(1)
    return print("自动调度流程无人接单！若调度人工派单请忽略！")


# 加密报文：加签
def get_security_code(request_list):
    # print("request_list:", request_list)
    url = "http://testinsapi.cias.cn:30011/zbcf-casecenter/tester/encode"
    headers = {"Content-Type": "application/json"}
    data_body = request_list['json']
    res = requests.post(url, data=json.dumps(data_body), headers=headers)
    request_result = res.json()
    request_data = request_result['data']
    request_data_sign = request_data['sign']
    request_data_data = request_data['data']
    request_body = {'sign': request_data_sign, 'data': request_data_data}
    # print('body', request_body)
    # 覆盖原来的request_list里json键值
    request_list['json'] = request_body
    # print("加密后的：", request_list)
    # print("派单接口状态：" + str(res.status_code))
    return request_list


# 获取用户user_id
def get_user_id(login_name):
    # user_id_value = MySqlOperate().get_one_encryption_column_value('zbcf_business_test.t_us_login', 'mobile', mobile, 'id')
    user_id_value = MySqlOperate().get_one_column_value('zbcf_business_test.t_us_login', 'login_name', login_name, 'id')
    try:
        if user_id_value:
            print("user_id_value:", user_id_value)
            return str(user_id_value)
    except Exception as e:
        print("兼业人员接单失败，中台无订单！", e)

# 根据手机号码获取memberid
def get_member_id(mobile):
    memberid = MySqlOperate().get_one_encryption_column_value('zbcf_business_test.t_us_member_info', 'mobile', mobile, 'id')
    return memberid

# 获取公司id
def get_company_id_value(company_name):
    company_id_value = MySqlOperate().get_one_column_value('zbcf_business_test.t_us_company_info', 'company_name', company_name, 'id')
    return company_id_value


# 获取订单号order_no
def get_order_no(report_no):
    order_no_value = MySqlOperate().get_one_column_value('zbcf_business_test.t_od_order', 'case_no', report_no, 'order_no')
    # print("order_no_value:", order_no_value)
    return order_no_value


# 获取任务编号task_id
def get_task_id(report_no):
    task_id_value = MySqlOperate().get_one_column_value('zbcf_business_test.t_cs_task_info', 'case_no', report_no, 'id')
    try:
        if task_id_value:
            print("task_id_value:", task_id_value)
        return task_id_value
    except Exception as e:
        print("无订单可以销案！", e)


# 获取事故单确认状态
def get_confirm(order_no):
    confirm_value = MySqlOperate().get_one_column_value('zbcf_business_test.t_wk_parttime_survey', 'order_no', order_no, 'confirm')
    print("confirm_value:", confirm_value)
    return confirm_value


# 获取公司编码：company_id
def get_company_id(report_no):
    company_id_value = MySqlOperate().get_one_column_value('db_zbcf_casecenter_test.t_report_info', 'report_no', report_no, 'company_id')
    print("company_id:", company_id_value)
    return company_id_value


# 获取兼业作业ID：work_id
def get_work_id(order_no):
    work_id_value = MySqlOperate().get_one_column_value('zbcf_business_test.t_wk_parttime_survey', 'order_no', order_no, 'id')
    print("id:", work_id_value)
    return work_id_value


# 获取：survey_model_id
def get_survey_model_id(report_no):
    survey_model_id_value = MySqlOperate().get_one_column_value('zbcf_business_test.t_wk_survey_model', 'case_no', report_no, 'id')
    print("id:", survey_model_id_value)
    return survey_model_id_value


# 获取car_model_id
def get_car_model_id(report_no):
    car_model_id_value = MySqlOperate().get_one_column_value('zbcf_business_test.t_wk_car_model', 'case_no', report_no, 'id')
    print("id:", car_model_id_value)
    return car_model_id_value


# 获取案件状态 order_status

def get_order_status(report_no):
    order_status = MySqlOperate().get_one_column_value('zbcf_business_test.t_od_order', 'case_no', report_no, 'order_status')
    # print('status:', order_status)
    return order_status


# 获取partner服务的内部workid
def get_partner_taskid(reportno):
    # 获取案件在系统中的taskid
    taskid = get_task_id(reportno)
    sql = "SELECT task_id FROM zbcf_partner_test.t_partner_operate_record WHERE task_id like '%s%%' and provider !='共享公司'  order by id  desc  LIMIT 1"%taskid

    workid = MySqlOperate().mysql_execute(sql)
    print("获取partner服务的内部workid为",workid)
    return workid


# 打印request请求
def get_message(request):
    print("Print the message:", request)


# 顺丰请求平台接口数据加签
def sf_encrypt(request):
    encrypt_body = {}
    print('顺丰加密前的接口是...', request)
    data_body = request.get('json')
    data_base64 = base64.b64encode(json.dumps(data_body).encode())
    h1 = hmac.new(bytes("111",'utf-8'), data_base64, digestmod=hashlib.sha1).hexdigest()
    encrypt_body['sign'] = h1
    encrypt_body['data'] = data_base64.decode(encoding='utf-8')
    request['json'] = encrypt_body
    print('顺丰加密后的接口是...', request)


# APP 登录数据加密
def login_encrypt_app(request):
    app_encrypt_public_key = os.environ['app_encrypt_public_key']
    app_sign_private_key = os.environ['app_sign_private_key']
    pre_encrypt_data = data_body = request.get('json')
    # 对密码进行md5处理
    m = hashlib.md5()
    m.update((data_body.get('loginPass')+'ZBCF_BDE5EE74026640FCB2EBD8BF059098D2').encode('utf-8'))
    passwd_md5 = m.hexdigest()

    pre_encrypt_data['loginPass'] = passwd_md5
    encrypt_param ={
        "text": json.dumps(pre_encrypt_data),
        "encryptPublicKey": app_encrypt_public_key,
        "signPrivateKey": app_sign_private_key
    }
    print('加密请求接口数据为：', encrypt_param)
    url = 'http://10.3.200.99:8080/auto-test-help/rsa/encrypt.do'
    headers = {'content-type': 'application/json;charset=UTF-8'}
    res = requests.post(url, data=json.dumps(encrypt_param), headers=headers)
    obj = res.json()
    print('加密后的数据为：', obj)
    request['json'] = obj.get('resultObject')


# 对APP登录结果进行解密
def login_decrypt_app(response):
    app_encrypt_public_key = os.environ['app_encrypt_public_key']
    app_sign_private_key = os.environ['app_sign_private_key']
    data_response = response.json
    print('解密前的响应数据：', data_response)
    if data_response.get('data') and data_response.get('sign'):
        decrypt_param = {
            "text": data_response.get('data'),
            "sign": data_response.get('sign'),
            "validSignPublicKey": app_encrypt_public_key,
            "decryptPrivateKey": app_sign_private_key
        }
    url = 'http://10.3.200.99:8080/auto-test-help/rsa/decrypt.do'
    headers = {'content-type': 'application/json;charset=UTF-8'}
    res = requests.post(url, data=json.dumps(decrypt_param), headers=headers)
    response.json = res.json()['resultObject']
    print('解密后的数据：', response.json)


# int类型转换为string
def toString(value):
    print(value, type(value))
    return str(value)


# base64解密
def base64_decrypt(data):
    print("解密前的加密串: \n ",data)
    decrypt_data = base64.b64decode(data.encode('utf-8')).decode('utf-8')
    print('解密后的字符串为\n',decrypt_data)
    return str(decrypt_data)


# 保险公司mock数据解密
def handle_mockdata(response):
    data_response = response.json
    print('data_response,',data_response)
    response.json = json.loads(base64_decrypt(data_response.get('data')))
    print('解密后的保险公司mock数据为：\n',response.json)

# 调度系统登录页获取验证码
def get_verifyCode(cookie):
    formlist = cookie.split(";")
    for form in formlist:
        if form.startswith('SESSION'):
            session = form.split('=')[1]
            break
    print('session is ',session)
    radisname = 'spring:session:sessions:'+session
    print(radisname)
    radiskey = 'sessionAttr:session_validate_code'
    radis = RedisHandle()
    radisvalue = radis.gethashvalue(radisname,radiskey)
    print(radisvalue)
    verifyCode = radisvalue[-4:].decode()
    print('获取到的调度系统验证码为：',verifyCode)

    return verifyCode


if __name__ == "__main__":
    # cookie = 'SESSION=313e1b4f-cb63-4f77-9318-6e97f8c13fc0; JSESSIONID=6F205A0EF8B77A0D3CD7F493A04E87B3; um_distinct_id=eb6c8398ca7d4a228ea7244382179602;'
    # print(get_verifyCode(cookie))

    is_order_taked('AutoPortosZC20190530150340')
