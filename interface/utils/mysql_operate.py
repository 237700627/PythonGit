# -*- coding:UTF-8 -*- 
# Author:hanbo(Portos)
# Datetime:2019/2/21 16:04
# Project:PyCharmPro
"""
函数说明：
1、此类用作：连接数据库，并执行SQL语句；
2、调用mysql_execute函数时，直接传入相应的sql语句即可，每次只能传一条sql语句，执行结果为数组；
"""
import pymysql


class MySqlOperate:
    # 初始化参数
    def __init__(self):
        self.host = 'rm-wz97oujls3998784i.mysql.rds.aliyuncs.com'
        self.user = 'testuser'
        self.password = 'testuser@2018'
        self.con = pymysql.connect(host=self.host, user=self.user, password=self.password)
        self.cur = self.con.cursor()

    # 执行整条SQL语句
    def mysql_execute(self, sql_statement):
        print('数据库语句为：', sql_statement)
        # 执行增删改查的sql语句
        try:
            if sql_statement.strip().upper().startswith('INSERT'):
                # 增
                self.cur.execute(sql_statement)
            elif sql_statement.strip().upper().startswith('DELETE'):
                # 删
                self.cur.execute(sql_statement)
            elif sql_statement.strip().upper().startswith('UPDATE'):
                # 改
                self.cur.execute(sql_statement)
            elif sql_statement.strip().upper().startswith('SELECT'):
                # 查
                self.cur.execute(sql_statement)

                # 获取连接对象的描述信息（即表头信息）
                index = self.cur.description

                try:
                    # 获取所有数据，得到一个元组
                    data = self.cur.fetchall()
                    # print('All data:', data)
                    if not data:
                        print("查询数据为空，请重新输入查询语句！")

                    # 将元组转换为数组，使之可以根据Key得到Value
                    result = []
                    # 获取只有一行一列的值
                    if len(index)-1 == 0:
                        result = data[0][0]
                        return result
                    else:
                        for res in data:
                            row = {}
                            for i in range(len(index)):
                                row[index[i][0]] = res[i]
                                result.append(row)
                            return result
                except Exception as e:
                    print('请检查SQL语句', e)
            else:
                print('Please input sql statement begin with "INSERT","DELETE","UPDATE","SELECT"!')
        except Exception as e:
            self.con.rollback()  # 事务回滚
            print('SQL语句有误，事务处理失败，已回滚事务！', e)
        else:
            self.con.commit()  # 事务提交

    # 查询未加密字段值：根据条件，获取某个指定字段的值，传入：db.table，条件列和值，查询列名
    def get_one_column_value(self, db_table_name, condition_column_name, condition_column_value, select_column_name):
        sql_statement = "SELECT * FROM " + db_table_name + " " \
                        "WHERE " + condition_column_name + " = '" +\
                        str(condition_column_value) + "';"

        data_info = self.mysql_execute(sql_statement)
        # print("data_info:", data_info)
        try:
            if data_info:
                # 获得指定列的值
                select_column_value = data_info[0].get(select_column_name)
                # print("select_column_value:", select_column_value)
                return select_column_value
        except Exception as e:
            return print("获取结果为空！原因：", e)

    # 查询加密字段值：根据条件，获取某个指定字段的值，传入：db.table，条件列和值，查询列名
    def get_one_encryption_column_value(self, db_table_name, condition_column_name, condition_column_value,
                                        select_column_name):
        # 先使用加密语句，查询出条件语句中，条件值的加密结果
        encryption_sql = "SELECT HEX(AES_ENCRYPT('" + str(condition_column_value) + "','ZBCFaes9527@cias'));"
        # print(encryption_sql)
        encryption_data = self.mysql_execute(encryption_sql)
        # print(encryption_data)
        try:
            sql_statement = "SELECT * FROM " + db_table_name + " " \
                            "WHERE " + condition_column_name + " = '" + \
                            encryption_data + "';"
            data_info = self.mysql_execute(sql_statement)
            # print("data_info:", data_info)
            if data_info:
                select_column_value = data_info[0].get(select_column_name)
                # print("select_column_value:", select_column_value)
                return select_column_value
        except Exception as e:
            return print("获取结果为空！原因：", e)

    def __del__(self):
        self.cur.close()
        self.con.close()


if __name__ == '__main__':
    '''
    test_data = MySqlOperate().mysql_execute("SELECT * FROM zbcf_business_test.t_od_order WHERE case_no = 'AutoPortosHA20190425163428';")
    print('-----------------')
    print('test_data:', test_data)
    
    test_data = MySqlOperate().get_one_encryption_column_value('zbcf_business_test.t_us_login', 'mobile', '17000000002', 'id')
    print(test_data)
    '''
    test_data = MySqlOperate().mysql_execute("select HEX(AES_ENCRYPT('17000000002','ZBCFaes9527@cias'));")
    print(test_data)
