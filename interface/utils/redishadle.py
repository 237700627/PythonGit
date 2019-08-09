# -*- coding:UTF-8 -*-
# Author:wubin(Adom)
# Datetime:2019/2/21 17:53
"""
函数说明：
1、本函数为链接redis数据库，并执行增删改查操作；
2、调用函数时，先引包“from redishandle import RedisHandle”,在使用相关方法即可
"""
import redis

#redis操作类
class RedisHandle():

    def __init__(self):
        pool = redis.ConnectionPool(host='10.3.200.101', port=6379,password='tt3&cmQ8UB',decode_responses=False)
        self.r = redis.Redis(connection_pool=pool)

     # 在Redis中设置值，默认，不存在则创建，存在则修改
     # 参数：
     # ex，过期时间（秒）
     # px，过期时间（毫秒）
     # nx，如果设置为True，则只有name不存在时，当前set操作才执行
     # xx，如果设置为True，则只有name存在时，当前set操作才执行
    def setvalue(self,name, value, ex=None, px=None, nx=False, xx=False):
        value = self.r.set(name, value, ex=None, px=None, nx=False, xx=False)
        return value

    #设置值，只有name不存在时，执行设置操作（添加）
    def setnxvalue(self,name,value):
        value = self.r.setnx(name, value)
        return value

    # 设置值
    # 参数：
    # time，过期时间（数字秒 或 timedelta对象）
    def setexvalue(self,name, value, time):
        value = self.r.setex(name, value, time)
        return value

    # 设置值
    # 参数：
    # time_ms，过期时间（数字毫秒 或 timedelta对象）
    def psetexvalue(self,name, time_ms, value):
        value = self.r.psetex(name, time_ms, value)
        return value

    #批量设置值
    #如：
    #   mset(k1='v1', k2='v2')
    #   或
    #   mget({'k1': 'v1', 'k2': 'v2'})
    def msetvalue(self,*args,**kwargs):
        value = self.r.mset(*args, **kwargs)
        return value

    #根据key获取String类型value值
    def getvalue(self,key):
        value = self.r.get(key)
        return value

    #根据key 获取hash类型的value值
    def gethashvalue(self,name,key):
        value = self.r.hget(name,key)
        return value

    #批量获取
    #如：
    # mget('name', 'root')
    # 或
    # r.mget(['name', 'root'])
    def mgetvalue(self,keys, *args):
        value = self.r.mget(keys, *args)
        return value

    #设置新值并获取原来的值
    def getsetvalue(self,name, value):
        value = self.r.getset(name, value)
        return value

if __name__ == "__main__":
    pool = redis.ConnectionPool(host='10.3.200.101', port=6379, password='tt3&cmQ8UB', decode_responses=False)
    r = redis.Redis(connection_pool=pool)
    keys = r.keys()
    print(keys)
    print(r.hkeys('spring:session:sessions:71796486-158a-4f8a-ad26-7799bbd00a2f'))
    # print(r.hgetall('spring:session:sessions:313e1b4f-cb63-4f77-9318-6e97f8c13fc0'))
    b = r.hget('spring:session:sessions:71796486-158a-4f8a-ad26-7799bbd00a2f','sessionAttr:session_validate_code')

