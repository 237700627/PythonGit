# 广西南宁租赁管理系统 
#### 该仓库主要为广西南宁租赁管理系统支持API冒烟测试使用

#### 账号信息
##### 1. C端：
- 测试一号: 19812345678 abc123 房东账号 110101199003075779
- 测试二号: 19822345678 abc123 租客账号 110101199003070011
- 个人房东: 18312506961 abc123 朱慧 411526198805063821  房屋所有权证号 所有权证号203

##### 2. B端：
- 中介公司: 17773491179 abc123 刘杨玉账号
- 开发企业: 18923807539 abc123 蒋金家账号
- 国有企业: 13113010028 abc123 孙阳阳账号
- 租赁企业: 13681854237 abc123 傅强账号

##### 3. G端：
- 管理员: admin zfSTD1501

##### 4. gxnn_config.py
- 配置文件: DB连接信息、redis连接信息、跳板机、请求url等配置

##### 5. 注意： B端和C端账号由testcases_init生成
- 主要生产C端测试一号、测试二号账号
- B端状态为默认状态，若删除，则需要新建

#### 调用方法信息
##### 1. debugtalk.py 方法介绍
    1. get_url(**kwargs)   # post 转 get
    2. conn_mysql(insql, db='govzf_pahf_zulin_db', inregex='\D') # 执行sql，返回查询结果
    3. conn_mysql_sms(insql, inregex='\D')  # 获取短信验证码
    4. get_random_num(s_num, e_num) # 获取随机数，默认为0-100之间的整数
    5. dict_key_choice(in_dict, in_key, in_r=0) # 字典取值
    6. get_value_from_list(list_v)  # 从list里面随机取其中一个值
    7. get_value_from_sql(in_sql)   # 更加sql查询到的值随机取其中一个
    8. get_date(num=0, frm='%Y-%m-%d')  # 获取时间
    9. base64key(file_path) # 将图片转成base64数据流
    10.conn_redis() # 连接redis
    11.get_redis_imgcode(*args) # 从redis里获取图形验证码或短信验证码
    12.del_redis_failtimes()    # 删除redis登录失败次数
    13.get_house_id_from_html() # 从html里抓取第一个houseId

##### 2. httprunner自带的常用方法
    1. gen_random_string(str_len)  # 生成随机字符串
    2. get_timestamp(str_len=13)  # 获取时间戳，最长16位
    3. get_current_date(fmt="%Y-%m-%d") # 获取当前时间，传时间格式
    4. multipart_encoder(field_name, file_path, file_type=None, file_headers=None) # 处理上传文件方法
