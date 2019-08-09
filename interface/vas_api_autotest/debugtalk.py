# -*- coding:UTF-8 -*- 
# Author:hanbo(Portos)
# Datetime:2019/5/25 17:30
# Project:PyCharmPro

import base64
import hmac
import json
import os
import time
import uuid
from hashlib import sha1

import requests
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from faker import Faker

from utils.AES_util import Aes_utils
from utils.mysql_operate import MySqlOperate


# 获取配置文件配置
def get_config(key):
    value = os.environ.get(key)
    return value


# 对字符串进行base64编译
def get_base_64_code(input_code):
    out_code = base64.b64encode(input_code.encode('utf-8')).decode('utf-8')
    return out_code


# 获取系统当前时间戳，int类型
def get_current_time():
    current_time = str(int(round(time.time())))
    return current_time


# 自定义名称：适用于不重复名称（不算name参数，已经有15各字符）
def get_customize_name(name):
    customize_name = name + time.strftime('%Y%m%d%H%M%S') + str(round(3))
    # print(customize_name)
    return customize_name


# 拼接cookie
def get_cookie_str(token):
    cookie = 'token=' + token
    return cookie


# APP端请求数据做AES加密
def aesencrypt(json_data, AES_key):
    print('加密前的数据为：', json_data)
    str_data = json.dumps(json_data)

    encrypt = Aes_utils()

    encrypt_data = encrypt.encrypt(str_data, AES_key)
    return encrypt_data


# 对数据进行hmacsha1加密签名
def hmacsha1(json_data, key):
    # hmac_code = hmac.new(key.encode(), json.dumps(json_data).encode(), sha1)
    print('加签秘钥为：',key)
    hmac_code = hmac.new(key.encode(), json_data.encode(), sha1)
    return hmac_code.hexdigest()


# 生成uuid
def get_uuid():
    return str(uuid.uuid1()).replace('-', '')


# 获取系统当前时间：yyyy-MM-dd HH:mm:ss
def get_local_time_format():
    local_time_format = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(local_time_format)
    return local_time_format


# APP 业务数据加密加签
def request_encrypt(request, aesKey, signKey):
    requestdata = request['json']
    print('加密前的业务参数数据为：',requestdata)
    encryptdata = {'requestId':str(uuid.uuid1()).replace('-',''),'requestTime':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),'version':'1.0'}
    encryptdata['data'] = str(aesencrypt(requestdata,aesKey))
    signdata = encryptdata['requestId']+encryptdata['requestTime']+encryptdata['version']+encryptdata['data']
    encryptdata['sign'] = hmacsha1(signdata,signKey)
    request['json'] = encryptdata


# APP业务数据解密
def response_decrypt(response,aeskey):
    resppnse_data = response.json['data']
    print('解密前的响应数据：', resppnse_data)
    aes_util = Aes_utils()
    decrypt_data  =  json.loads(aes_util.decrypt(resppnse_data,aeskey))
    print('解密后的响应数据为：',decrypt_data)
    response.json['data'] = decrypt_data
    

# APP登录用户名密码数据加密
def login_encrypt_app(request):
    print('登录数据为：',request)
    app_encrypt_public_key = os.environ['app_encrypt_public_key']
    data_body = request.get('json')

    loginname_encrypt = rsa_encrypt(app_encrypt_public_key,data_body['userName'])
    passwd_encrypt = rsa_encrypt(app_encrypt_public_key,data_body['password'])

    data = {"password":passwd_encrypt,'userName':loginname_encrypt}

    requestdata = {"data": json.dumps(data),"requestId":get_uuid(),"requestTime":get_local_time_format(),"sign":"","version":"1.0"}

    print('处理后的登录数据为：',requestdata)
    request['json'] = requestdata


# 响应数据data转换
def response_to_obj(response):
    response_data = response.json
    data = response_data['data']
    if data:
        response.json['data'] = json.loads(data)
    else:
        pass


# 获取用户在用户中心登录cookie，需要三个步骤
# 第一步：获取重定向的accesskey
def get_access_key(host='http://testum.cias.cn'):
    url_1 = host + '/usercenter/public/resource/authcUser'
    # 请求url_1获取accesskey
    response = requests.get(url_1)
    # 获取响应的json数据转换成字典格式
    res = response.json()
    # print('1', res)
    # print(rps['data']['redirect'])

    # 截取res中的accesskey
    # 例如：'redirect': 'http://testum.cias.cn/passport/login?accessKey=MVpmRDZVZHkyWThqNFJmaThNZUcwSTEyY044ajRsNWk%3D'
    access_key_value = str(res['data']['redirect']).split('=')[1]
    access_key = str(access_key_value).split('%')[0]
    # print('2', access_key)
    return access_key


# 第二步：获取um_distinct_id，请求该接口以后,会在cookie中设置一个唯一值,用于校验验证码,登录失败次数等
def get_um_distinct_id(host='http://testum.cias.cn'):
    url_2 = host + '/usercenter/public/auth/umDistinct'
    response = requests.get(url_2)
    # print(response.status_code)

    if response.status_code == 200:
        # print("获取cookies" + str(response.cookies))
        # for cookie in html_2.cookies:
            # print("打印cookie" + str(cookie))
        um_distinct_id = str(response.cookies).split(' ', 2)[1]
        # print(um_distinct_id)
    return um_distinct_id


# 第三步：获取登陆后的cookie
def get_cookie(username, pwd, host='http://testum.cias.cn', channel='usernamePwd', user_type='1', origin_type='PC'):
    # 对密码pwd进行base64编译
    pwd = base64.b64encode(pwd.encode('utf-8')).decode('utf-8')
    url_3 = host + '/usercenter/public/auth/login'
    headers = {
        "Host": host.split('//')[1],
        "Content-Type": 'application/json;charset=UTF-8',
        # 拼接重定向访问的url
        "Referer": host + "/passport/login?accessKey=" + get_access_key() + "&redirect_url=http%3A%2F%2Fdevvas.cias.cn%2Foss%2F%23%2Findex",
        "cookie": get_um_distinct_id()
    }
    data = {
        "channel": channel,
        "accessKey": get_access_key() + '=',
        "userType": user_type,
        "loginInfo": {
            "code": "",
            "username": username,
            "pwd": pwd,
            "originType": origin_type,
            "partnerId": ""
        }
    }
    res = requests.post(url=url_3, data=json.dumps(data), headers=headers)
    res_data = res.json()
    # print("登陆状态" + str(h3['code']))
    if int(res_data['code']) == 200:
        ck_data = str(res.cookies).split(' ', 2)
        cookie = ck_data[1]
        print('登陆成功，获取cookie:' + cookie)
    else:
        # print(str(res_data['code']) + '\n' + str(res_data["message"]))
        print(res_data)
    # print(res.headers['Set-Cookie'])
    return cookie
    # return res.headers['Set-Cookie']


# RSA 加密
def rsa_encrypt(pub_key_text, text):
    pub_key_text = '-----BEGIN PUBLIC KEY-----\n{}\n-----END PUBLIC KEY-----'.format(pub_key_text)
    rsakey = RSA.importKey(pub_key_text)
    cipher = PKCS1_v1_5.new(rsakey)
    cipher_text = cipher.encrypt(text.encode('utf-8'))
    cipher_text = base64.b64encode(cipher_text)
    return cipher_text.decode('utf-8')


# 加签算法
def hash_hmac(key, text):
    hmac_code = hmac.new(key.encode(), text.encode(), sha1)
    # print("text:", text)
    return hmac_code.hexdigest()


# 组装请求参数
def sign_api(sign_key='', param={}, ver='1.0'):
    """
    ajax请求api
    :param sign_key: 秘钥
    :param param: 入参对象
    :param ver: 版本
    :return: 返回值对象
    """
    print("sign_key的值为:", sign_key)
    # 获取请求body参数值
    request_id = get_uuid()
    request_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    version = ver
    json_data = param['json']
    data = json.dumps(json_data)

    if sign_key:
        # 加签
        sign = hash_hmac(sign_key, '%s%s%s%s' % (request_id, request_time, version, data))
    else:
        sign = ''

    obj_data = json.loads(data)

    # 重新组装body
    body = {
        'requestId': request_id,
        'requestTime': request_time,
        'version': version,
        'sign': sign,
        "data": json.dumps(obj_data)
    }
    # 覆盖原request中的json值
    param['json'] = body
    print("body组装后为:", param['json'])
    return param


# 获取产品名称
# def get_product_name(product_name):
#     product_name_value = MySqlOperate().get_one_column_value('zbcf_vas_test.t_product', 'product_name', product_name, 'product_name')
#     print("product_name_value:", product_name_value)
#     return product_name_value


# 查询未加密字段值：根据条件，获取某个指定字段的值，传入：db.table，条件列和值，查询列名
def get_column_value(db_table_name, condition_column_name, condition_column_value, select_column_name):
    select_column_value = MySqlOperate().get_one_column_value(db_table_name, condition_column_name, condition_column_value, select_column_name)
    print("select_column_value:", select_column_value)
    return select_column_value


# #################################### 以下为各种生成随机数函数集 Start #################################### #
# 生成faker对象
f = Faker(locale='zh_CN')
"""
- 普通车牌
- 特种车牌
- 新能源小型车车牌
- 新能源大型车车牌
- 可以自定义生成车牌
- 可以生成不同省市机构发型的车牌
"""
license_plate_provinces = (
        "京", "沪", "浙", "苏", "粤", "鲁", "晋", "冀",
        "豫", "川", "渝", "辽", "吉", "黑", "皖", "鄂",
        "津", "贵", "云", "桂", "琼", "青", "新", "藏",
        "蒙", "宁", "甘", "陕", "闽", "赣", "湘"
    )
license_plate_letter = (
        "A", "B", "C", "D", "E", "F", "G", "H",
        "J", "K", "L", "M", "N", "P", "Q", "R",
        "S", "T", "U", "V", "W", "X", "Y", "Z"
    )
license_plate_num = (
        "A", "B", "C", "D", "E", "F", "G", "H",
        "J", "K", "L", "M", "N", "P", "Q", "R",
        "S", "T", "U", "V", "W", "X", "Y", "Z",
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"
    )
license_plate_last = ("挂", "学", "警", "港", "澳", "使", "领")


# 随机生成普通车牌
def get_license_plate():
    # 临时方案：直接随机生成
    plate = "{0}{1}{2}".format(f.random_element(license_plate_provinces),
                               f.random_element(license_plate_letter),
                               "".join(f.random_choices(elements=license_plate_num, length=5)))
    # print("普通车牌号：{}".format(plate))
    # 终极方案：去重随机生成
    return plate


# 随机生成去重手机号
def get_mobile():
    while True:
        mobile = f.phone_number()
        has_mobile = get_column_value('zbcf_usercenter_test.t_person', 'mobile', mobile, 'mobile')
        if not has_mobile:
            print("手机号是：{}".format(mobile))
            return mobile


# 随机生成姓名
def get_name():
    name = "自动化" + f.name()
    print("姓名：{}".format(name))
    return name
# #################################### 以上为各种生成随机数函数集 End #################################### #


if __name__ == '__main__':
    # a = hmacsha1('5d7166c1428b45828bc84f8c1d52d0bf2019-07-04 15:19:011.0DIu9X1wqfX5Drz5U2s4cCo8WvfLY2sXEmuT1lEU+6clf3dYu+dq3ZY1RargqEdVh','5313BA838C8F071C')
    # print(a)
    # get_cookie('portos', '123456')
    # sign_api(method='GET', is_sign=False)
    # get_local_time_format()
    # get_customize_name('自动化产品测试')
    # get_column_value('zbcf_vas_test.t_product', 'id', 34, 'enable')
    # get_name()
    a = get_config("web_url")
    print(a)
