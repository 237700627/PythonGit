import os
import re
# import pymysql
import redis
import json
import random
import time
import base64
import rsa
from requests_toolbelt import MultipartEncoder
from sshtunnel import SSHTunnelForwarder  # pip install --proxy="10.28.80.246:8080" sshtunnel
# from config import base_c, base_b, base_g
from config import url
from config import pubkey
from config import project_db_host, project_db_user, project_db_password, project_db_name, project_db_port
from config import sms_db_host, sms_db_user, sms_db_password, sms_db_name, sms_db_port
from config import ssh_host, ssh_username, ssh_password, redis_host, redis_port, redis_db_name

# base_url_g = base_g
# base_url_b = base_b
# base_url_c = base_c


def base_url():
    default_request = {
        'base_url': url,
        'headers': {
            "Content-Type": "application/json;charset=UTF-8"}
    }
    return default_request['base_url']


def get_url(**kwargs):
    """
    将post请求数据转成get
    :param kwargs:
    :return:
    """
    pop_url = kwargs.pop('url')
    r_url = pop_url + '?'
    for k, v in kwargs.items():
        if isinstance(v, int):
            v = str(v)
        elif isinstance(v, float):
            v = str(v)
        # print('--->', k, v, r_url)
        r_url = r_url + k + '=' + v + '&'
    return r_url[:-1]


def conn_mysql(insql, inregex='\D', count='fetchone', host=project_db_host, user=project_db_user, password=project_db_password, db_name=project_db_name, port=project_db_port):
    """
    # 执行sql语句
    :param insql: 输入sql
    :param inregex: 正则,默认为获取数字
    :param count:   获取数量，默认为获取1个，其他获取全部
    :return:
    """
    # host = 'st-mysql-m.a.pa.com'
    # user = 'hfqa'
    # password = 'qn3p@bI0qg'
    # db_name = 'govzf_pahf_zulin14_db'
    # port = 3306
    print(insql)
    conn = pymysql.connect(host=host, user=user, passwd=password, port=port, db=db_name, charset='utf8')
    cur = conn.cursor()
    exc_type = str(insql).strip().split(' ')[0]
    cur.execute(insql)
    if count != 'fetchone':
        data = cur.fetchall()
        new_list = []
        for i in list(data):
            n_str = str(i).strip('()').strip(',').strip("'")
            new_list.append(n_str)
        return new_list
    if inregex == '' or exc_type.upper() != 'SELECT':
        if inregex == '':
            data = cur.fetchone()
        else:
            data = (2,)
        conn.commit()
        return data[0]
    else:
        data = str(cur.fetchone())
        r_tmp = re.sub(inregex, '', data)
        conn.commit()
        # print(r_tmp)
        return r_tmp


def conn_mysql_sms(mobile, host=sms_db_host, user=sms_db_user, password=sms_db_password, db_name=sms_db_name, port=sms_db_port):
    """
    获取短信验证码
    :param mobile:
    :param inregex:
    :return:
    """
    insql = 'SELECT sReplace FROM t_sms_log WHERE sMobile= %s ORDER BY iAutoID DESC LIMIT 1;' % mobile
    # host = 'st-mysql-m.a.pa.com'
    # user = 'hfqa'
    # password = 'qn3p@bI0qg'
    # db_name = 'service_db'
    conn = pymysql.connect(host=host, user=user, passwd=password, port=port, db=db_name, charset='utf8')
    cur = conn.cursor()
    cur.execute(insql)
    data = cur.fetchone()
    data_dict = json.loads(data[0])
    if 'code' in data_dict.keys():
        return data_dict['code']
    elif 'sms_content' in data_dict.keys():
        return data_dict['sms_content']
    else:
        return None


def dict_key_choice(in_dict, in_key, in_r=0):
    # 默认返回完整的value
    if in_r == 0:
        res = in_dict[in_key]
    # 返回value中的一项
    elif in_r == 1:
        res = random.choice(list(in_dict[in_key].keys()))
    # 以list方式返回value中多项
    elif in_r == 2:
        list_tmp = list(in_dict[in_key].keys())
        r_list = []
        # 获取返回list的随机长度
        list_long = random.randint(1, len(list_tmp))
        for i in range(list_long):
            key_tmp = list_tmp.pop(random.randint(0, len(list_tmp) - 1))
            r_list.append(key_tmp)
            res = r_list
    return res


def get_random_function_list(in_sql):
    func_list = conn_mysql(in_sql, count=1)
    return random.sample(func_list, random.randint(1, 10))


def get_value_from_sql(in_sql):
    get_list = conn_mysql(in_sql, count=1)
    if get_list and isinstance(get_list, list):
        res_index = random.randint(0, len(get_list) - 1)
        return get_list[res_index]
    else:
        return None


def get_value_from_list(list_v):
    if list_v and isinstance(list_v, list):
        index_key = random.randint(0, len(list_v) - 1)
        # print('-->', index_key, list_v[index_key])
        return list_v[index_key]
    else:
        # print('return False')
        return None


def get_random_num(s_num=0, e_num=100):
    """
    获取随机数
    :param s_num: 开始值
    :param e_num: 结束值
    :return:
    """
    if isinstance(s_num, int) and isinstance(e_num, int):
        return random.randint(s_num, e_num)
    else:
        return random.randint(0, 100)


def get_date(num=0, frm='%Y-%m-%d'):
    """
    func: 获取多少天后的日期(正数)或者多少天前的日期(负数)
    :param num:
    :param frm:
    :return:
    """
    if isinstance(num, int):
        return time.strftime(frm, time.localtime(time.time() + num * 24 * 60 * 60))
    else:
        return time.strftime(frm, time.localtime(time.time()))


def multipart_encoder_auto_files(file_path, file_type=None, file_num=1, field_path='files'):
    """
    :param file_path:
    :param file_type:
    :param file_num:
    :param field_path:
    :return:
    """
    fields = {}
    # 判断file_path是否为文件夹
    if os.path.isdir(file_path):
        # 判断非绝对路径的是否补全路径
        if not os.path.isabs(file_path):
            file_path = os.path.join(os.getcwd(), file_path)
        # 获取文件列表,补全文件的全路径
        files = [os.path.join(file_path, i) for i in os.listdir(file_path)]
        # 预提交的文件数必须在实际文件数内
        file_num = int(file_num)
        file_num = file_num if file_num < len(files) else len(files)
        # 遍历文件组装fields
        for i in range(file_num):
            # 随机获取文件
            file_tmp = random.choice(files)
            # 在files列表中删除取值，以防重复
            files.remove(file_tmp)
            # 文件杜绝使用类似命名：abc.abc.png
            filename = os.path.basename(file_tmp).split('.')[0]
            with open(file_tmp, 'rb') as f:
                fields[field_path] = (filename, f.read(), file_type)
            time.sleep(1)
    return MultipartEncoder(fields)


def base64key(file_path):
    # 判断非绝对路径的是否补全路径
    if not os.path.isabs(file_path):
        file_path = os.path.join(os.getcwd(), file_path)
    with open(file_path, 'rb') as f:
        data = base64.b64encode(f.read()).decode('utf-8')
    return data


def skiptest_true(new_bool):
    if new_bool:
        return True
    else:
        return False


def skip_del_tenant_apply(user_id):
    in_sql = 'SELECT COUNT(1) FROM t_tenant WHERE user_id in (%s) ;' % user_id
    count = conn_mysql(in_sql)
    if int(count) >= 80:
        del_sql = 'DELETE FROM t_tenant WHERE user_id in (%s) ;' % user_id
        conn_mysql(del_sql)
        return True
    else:
        return False


def conn_redis(ssh_host=ssh_host, ssh_username=ssh_username, ssh_password=ssh_password, redis_host=redis_host, redis_port=redis_port, db_name=redis_db_name):
    """redis连接"""
    local_port = get_random_num(12000, 13000)
    server = SSHTunnelForwarder(
        ssh_address_or_host=ssh_host,  # ssh地址 查看文档http://pms.ipo.com/pages/viewpage.action?pageId=99189559
        ssh_username=ssh_username,  # ssh连接的用户名
        ssh_password=ssh_password,  # ssh连接的用户名
        remote_bind_address=(redis_host, redis_port),  # 环境的redis ip和端口
        local_bind_address=('0.0.0.0', local_port))  # 指定一个本地端口号
    server.start()
    r = redis.Redis(host='127.0.0.1', port=server.local_bind_port, db=db_name, decode_responses=True)  # 本地转发host必须为127.0.0.1
    # r = redis.Redis(connection_pool=pool)
    return r, server


def get_redis_imgcode(*args):
    """获取redis数据"""
    # print('--->>', args, len(args))
    r, server = conn_redis()
    if 'SESSION=' in args[0]:
        start_num = args[0].find('SESSION=') + len('SESSION=')
        end_num = start_num + args[0][start_num:].find(';')
        session_tmp = args[0][start_num:end_num]
    try:
        if len(args) == 1 and 'SESSION=' in args[0]:
            hash_key = 'user:imgcode:{%s}' % session_tmp
            imgcode = r.hget(hash_key, session_tmp)
        elif len(args) == 2 and 'SESSION=' in args[0]:
            hash_key = 'user:msgcode:{%s}:{%s}' % (session_tmp, args[1])
            r_msgcode = r.hget(hash_key, session_tmp)
            imgcode = json.loads(r_msgcode)['code']
        elif len(args) == 3 and 'SESSION=' in args[0]:
            hash_key = 'user:msgcode:{%s}:{%s}:{$s}' % (session_tmp, args[1], args[2])
            r_msgcode = r.hget(hash_key, session_tmp)
            imgcode = json.loads(r_msgcode)['code']
        elif len(args) == 1 and 'SESSION=' not in args[0]:
            hash_key = 'reset:mobile:msgcode:{%s}:{%s}' % (args[0], args[0])
            r_msgcode = r.hget(hash_key, args[0])
            imgcode = json.loads(r_msgcode)['code']
        server.close()
        # print('--->', imgcode)
        return imgcode
    except Exception as e:
        server.close()
        return False


def del_redis_failtimes(mobile, del_name='login'):
    """删除redis里登录失败次数、人脸识别失败次数等"""
    r, server = conn_redis()
    if del_name=='login':
        del_key ='user:login:failtimes{%s}' % mobile
    elif del_name =='faceValidate':
        identity_sql= 'select identity from t_account where mobile = (%s)' % mobile
        del_key= 'user:faceValidate:failtimes{%s}' % conn_mysql(identity_sql)
    # 其他删除情况待拓展
    r.delete(del_key)
    server.close()


def get_house_id_from_html(res_body):
    res = re.findall('detail.id.\d*.html', res_body)
    house_id = res[0].split('.')[2]
    return house_id


def get_house_id(*args):
    pass


def str2key(public_key):
    # 对字符串解码
    b_str = base64.b64decode(public_key)
    if len(b_str) < 162:
        return False
    hex_str = ''
    # 按位转换成16进制
    for x in b_str:
        # print(x)
        h = hex(int(x))[2:]
        h = h.rjust(2, '0')
        hex_str += h
    # 找到模数和指数的开头结束位置
    m_start = 29 * 2
    e_start = 159 * 2
    m_len = 128 * 2
    e_len = 3 * 2
    modulus = hex_str[m_start:m_start + m_len]
    exponent = hex_str[e_start:e_start + e_len]
    return modulus, exponent


def password_encrypt(password):
    # pubkey = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCOOBZycDvWuX3kei/buHZ2wNhwSAjLP5oCJyjUQiunQPaBibunQm+6t+RMvh0up' \
    #          '/hhWgWvbeXgT1hCe1K9YJ6aOWCNrA0wYWEmQgfQ8NFvRp3DPd2ifF4DS55gG6mtDXSyQILSZhhPvzYWx70rdhnzekvMdJMdZMXRU+' \
    #          'q6RtvndQIDAQAB'
    key = str2key(pubkey)
    # print(key)
    modulus = int(key[0], 16)
    exponent = int(key[1], 16)
    rsa_pubkey = rsa.PublicKey(modulus, exponent)
    crypto = rsa.encrypt(password.encode(), rsa_pubkey)
    b64str = base64.b64encode(crypto)
    return b64str.decode()

