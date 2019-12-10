"""
============================
Author:cheer
# @time:2019-11-19 10:01
# @FileName: handle_mysql.py
# @Software: PyCharm
# @Cnblogs ：https://www.cnblogs.com/*****
============================
"""
import pymysql
import random
from scripts.handle_yaml import do_yaml
'''
类封装的原则：不同功能写不同的方法
'''

class HandleMysql(object):
    def __init__(self):
        # 1 建立连接
        # self.conn = pymysql.connect(host='api.lemonban.com',  # mysql服务器IP或者域名
        #                             user='future',  # 用户名
        #                             password='123456',  # 密码
        #                             db='futureloan',  # 要连接的数据库名
        #                             port=3306,  # 数据库端口号，默认为3306，也可以不写
        #                             charset='utf8',  # 数据库编码为utf8,不能写为utf-8
        #                             cursorclass=pymysql.cursors.DictCursor  # 添加游标类，取结果的时候返回的字典类型；不添加返回元组
        #                             )
        self.conn = pymysql.connect(host=do_yaml.read_yaml('mysql', 'host'),  # mysql服务器IP或者域名
                                    user=do_yaml.read_yaml('mysql', 'user'),  # 用户名
                                    password=do_yaml.read_yaml('mysql', 'password'),  # 密码
                                    db=do_yaml.read_yaml('mysql', 'db'),  # 要连接的数据库名
                                    port=do_yaml.read_yaml('mysql', 'port'),  # 数据库端口号，默认为3306，也可以不写
                                    charset='utf8',  # 数据库编码为utf8,不能写为utf-8
                                    cursorclass=pymysql.cursors.DictCursor  # 添加游标类，取结果的时候返回的字典类型（结果不唯一的话返回嵌套字典的列表）；不添加返回元组
                                    )
        # 2.创建游标对象
        self.cursor = self.conn.cursor()

    def run(self, sql, args=None, is_more=True):
        # 3.使用游标对象，运行sql
        self.cursor.execute(sql, args)
        # 4.使用连接对象提交
        self.conn.commit()
        # 5.返回结果
        if is_more:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchone()

    # 官方推荐，一定要关闭
    def close(self):
        self.cursor.close()
        self.conn.close()

    @staticmethod
    def create_mobile():
        """
        随机生成11位手机号
        :return:
        """
        return '188' + ''.join(random.sample('0123456789', 8))

    def is_existed_mobile(self, mobile):
        """
        判断手机号是否被注册
        :param mobile: 待判断是否注册的手机号
        :return:
        """
        # sql = "select * from member where mobile_phone = %s;"
        sql = do_yaml.read_yaml('mysql', 'select_user_sql')
        # 已注册（run函数返回数据，即if表达式为真），返回True；查询不到结果（None），返回False
        if self.run(sql, args=[mobile], is_more=False):
            return True
        else:
            return False

    def create_not_exsited_mobile(self):
        """
        随机生成一个在数据库中不存在的手机号
        :return:
        """
        while True:
            # 随机生成一个手机号码
            one_mobile = self.create_mobile()
            # 如果找到了未注册的手机号，跳出循环
            if not self.is_existed_mobile(one_mobile):
                break

        return one_mobile


if __name__ == '__main__':
    do_mysql = HandleMysql()  # 不建议放在main上面创建对象，因为有关闭

    sql_1 = 'select * from member LIMIT 0,10;'
    # sql_2 = "select * from member where mobile_phone = '13888888889';"
    #
    # print(do_mysql.run(sql_1))
    print(do_mysql.run(sql_1))

    # print(do_mysql.create_not_exsited_mobile())

    do_mysql.close()
