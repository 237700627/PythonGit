# -*- coding: utf-8 -*-
import requests
import json
import time
import hmac
from hashlib import sha1

from vas_api_autotest.debugtalk import get_cookie, get_uuid
from vas_api_autotest.vas_utils.vas_aes_util import encrypt, decrypt


# 环境参数，可选：[dev|test]
environment = 'test'
# 开发环境token值
# token = 'rTSHrzZxg7w90lz7NbVDm/KOJJIon7OHlbZqI3LgDMrPQfh3DdmI/UX+wGDDr9QMGd9APKSLUyyZGMS1vqfgYQ2lppLwBQg/xs0VBmJx7EMTaPWLE3qxx/UCL0YOhuX10xncNwM9Kua6BYZvkM9sNA=='

# 测试环境token值
cookie = get_cookie('portos', '123456')
token = cookie[6:]

aes_key = None
sign_key = None


# 加签算法
def __hash_hmac(key, text):
    hmac_code = hmac.new(key.encode(), text.encode(), sha1)
    return hmac_code.hexdigest()


# http&app请求
def request_api(api, param={}, method='POST', app_type='1', is_sign=True):
    """
    ajax请求api
    :param api: rap2定义的接口，例如：/common/adcode/query
    :param param: 入参对象
    :param method: http请求方法，可选：['GET'|'POST']
    :param app_type: 请求类型：0 - APP, 1 - H5
    :param is_sign: 是否加签
    :return: 返回值对象
    """
    global aes_key
    global sign_key
    # 获取请求body值
    request_id = get_uuid()
    request_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    version = '1.0'
    sign = ''
    data = json.dumps(param)

    # 判断是否加签加密
    if is_sign:
        # 缓存区不存在加密key，则实时获取，并缓存到全局变量
        if aes_key is None or sign_key is None:
            key_res = request_api('/common/key/get', method='GET', is_sign=False)
            if key_res['code'] != 0:
                raise Exception('获取加密key失败，error={}'.format(key_res['message']))
            aes_key, sign_key = key_res['data']['aesKey'], key_res['data']['signKey']

        # 判断是否加密
        if app_type == '0':
            data = encrypt(aes_key, data)

        # 生成签名
        sign = __hash_hmac(sign_key, '%s%s%s%s' % (request_id, request_time, version, data))

    # 构造请求URL
    url = 'http://{}vas.cias.cn/vas-web/{}'.format(environment, api)

    headers = {
        'content-type': 'application/json;charset=UTF-8',
        'appType': app_type
    }
    body = {
        'requestId': request_id,
        'requestTime': request_time,
        'version': version,
        'sign': sign,
        "data": data
    }

    if method == 'GET':
        res = requests.get(url, params=body, headers=headers, cookies={'token': token})
    else:
        res = requests.post(url, data=json.dumps(body), headers=headers, cookies={'token': token})
    obj = res.json()

    # 转换data值为对象类型
    if app_type == '0':
        obj['data'] = {} if obj['data'] == '' else json.loads(decrypt(aes_key, obj['data']))
    else:
        obj['data'] = {} if obj['data'] == '' else json.loads(obj['data'])

    return obj


if __name__ == '__main__':
    # 1.省市区查询
    area_list_res = request_api('/common/adcode/query', param={"areaCode": "000000"}, app_type='0')
    print('省市区查询:\n', area_list_res)

    # 1.标准产品列表
    product_res = request_api('/manage/product/list', app_type='0')
    print('标准产品列表:\n', product_res)

    # 9.获取服务器时间
    server_datetime_res = request_api('/common/time/get', is_sign=False)
    print('获取服务器时间:\n', server_datetime_res)

    # 16.APP密码登录
    from vas_api_autotest.vas_utils.vas_rsa_util import encrypt as rsa_encrypt
    rsa_pub_key = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCnN2bJvlMXJIUXWw00CSO2QWyQVqpa4LXdgIUCdW1shYSHGLlDzy5048vD9lr1w6JMb1LjfAPgZF1aMd0MRAC3MNVsi1S6upwBnIj7JokixwG10GiJKh+au/mmwzu2lrKj1DgZo3qQk6x7/aDFMz042ecilWXUMISMfvNbQeJjZQIDAQAB'
    param = {
        'userName': rsa_encrypt(rsa_pub_key, '15000000003'),
        'password': rsa_encrypt(rsa_pub_key, '123456')
    }
    login_res = request_api('public/app/worker/loginByPwd', param=param, is_sign=False)
    print('APP密码登录:\n', login_res)

    '''
    白名单URL："/common/file/upload", "/common/file/download", "/manage/order/export"
    非加签加密URL："/common/key/get", "/common/time/get", "/public/wxapp/client/login",
            "/public/wxapp/client/checkToken", "/public/app/worker/loginByPwd"
    '''
