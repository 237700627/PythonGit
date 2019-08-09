# def hello_args(para1, *args):
#     print("para1 :", para1)
#     for arg in args:
#         print("args:", arg)
#
#     print("type(args):", type(args))
#
#
# hello_args('hello', 'this', 'is', 'mc.meng')
# 连接数据库公用方法
import datetime
import time

import pymysql




def orderTimeOut(operation_id, database="zbcf_injury_test"):
    conn = pymysql.connect(host="rm-wz97oujls3998784i.mysql.rds.aliyuncs.com", user="testuser",
                           password="testuser@2018", database=database, charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    now = datetime.datetime.now()
    now = now.strftime('%Y-%m-%d %H:%M:%S')
    sql = "UPDATE t_auth_info t SET end_effect_time = '%s' WHERE t.operation_id = '%s'" % (now, operation_id)
    effectRows = cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return effectRows
# a = orderTimeOut(260)
# print(a)

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

class Solution(object):
    def twoSum(self, nums, target):
        i = 0
        while i < len(nums):
            j = i+1
            while j < len(nums):
                if nums[i]+nums[j] == target:
                    return [i,j]
                j+=1
            i+=1
        return None
        # 厉害的算法
        # dic = {}
        # for i in range(len(nums)):
        #     if nums[i] in dic:
        #         return [dic[nums[i]], i]
        #     else:
        #         dic[target - nums[i]] = i
a = Solution()
L = [1,2,7,12,88,9,76,52]
b = a.twoSum(L, 53)
print(b)



import random
from data import DistrictList
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
#
# a = generator()
# print(a[0], a[1])


#########test########



##########test#############


