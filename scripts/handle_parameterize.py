"""
============================
Author:cheer
# @time:2019-11-20 18:35
# @FileName: handle_parameterize.py
# @Software: PyCharm
# @Cnblogs ：https://www.cnblogs.com/*****
============================
"""
import re

from scripts.handle_mysql import HandleMysql
from scripts.handle_yaml import HandleYaml
from scripts.handle_path import USER_INFO_DIR
from scripts.handle_yaml import do_yaml


class Parameterize(object):
    """
    参数化类
    """
    # 创建yaml对象
    do_yaml_user = HandleYaml(USER_INFO_DIR)

    # 不存在的手机号
    not_existed_tel_pattern = r'{not_existed_tel}'  # 类属性
    # 不存在的会员ID
    not_existed_id_pattern = r'{not_existed_id}'

    # 会员(投资人)ID
    existed_investor_id_pattern = r'{investor_id}'
    # 已存在的手机号
    existed_tel_pattern = r'{investor_tel}'
    # 已存在手机号对应的密码
    existed_pwd_pattern = r'{investor_pwd}'

    # 借款人ID
    existed_borrower_id_pattern = r'{borrower_id}'
    # 借款人电话
    existed_borrower_tel_pattern = r'{borrower_tel}'
    # 借款人密码
    existed_borrower_pwd_pattern = r'{borrower_pwd}'

    # 管理员电话
    existed_admin_tel_pattern = r'{admin_tel}'
    # 管理员密码
    existed_admin_pwd_pattern = r'{admin_pwd}'

    # 标ID
    loan_id_pattern = r'{loan_id}'
    # 不存在的标ID
    not_existed_loan_id_pattern = r'{not_existed_loan_id}'

    @classmethod
    def to_parameter(cls, data):
        # 使用正则进行匹配得到包含未注册手机号的data
        if re.search(cls.not_existed_tel_pattern, data):
            # 创建数据库连接及游标对象
            do_mysql = HandleMysql()
            # 匹配得到含有未注册手机号的data
            data = re.sub(cls.not_existed_tel_pattern, do_mysql.create_not_exsited_mobile(), data)
            # 关闭数据库游标对象、连接
            do_mysql.close()

        # 已存在的手机号:投资人手机号
        if re.search(cls.existed_tel_pattern, data):
            # 匹配得到含有已存在的手机号的data
            data = re.sub(cls.existed_tel_pattern,
                          cls.do_yaml_user.read_yaml('investor', 'mobile_phone'), data)

        # 已存在手机号的密码：投资人密码
        if re.search(cls.existed_pwd_pattern, data):
            # 匹配得到含有已存在手机号的密码的data
            data = re.sub(cls.existed_pwd_pattern,
                          cls.do_yaml_user.read_yaml('investor', 'pwd'), data)

        # 会员ID：投资人ID
        if re.search(cls.existed_investor_id_pattern, data):
            # 匹配得到含有投资人会员ID的data
            data = re.sub(cls.existed_investor_id_pattern,
                          str(cls.do_yaml_user.read_yaml('investor', 'user_id')), data)

        # 不存在的投资人ID
        if re.search(cls.not_existed_id_pattern, data):
            # 创建数据库连接及游标对象
            do_mysql = HandleMysql()
            # 配置文件中获取sql
            # 这里也可以不把sql语句写入配置文件，直接将sql语句写在下面
            sql = do_yaml.read_yaml('mysql', 'select_user_max_id_sql')
            # 运行sql，得到一个字典
            res_max = do_mysql.run(sql, is_more=False)
            # 获取字典的值，转换为字符串，将原data进行参数化
            data = re.sub(cls.not_existed_id_pattern,
                          str(res_max.get('max(id)') + 1), data)
            # 关闭数据库游标对象、连接
            do_mysql.close()

        # 借款人ID
        # 正则匹配：查找
        if re.search(cls.existed_borrower_id_pattern, data):
            data = re.sub(cls.existed_borrower_id_pattern,
                          str(cls.do_yaml_user.read_yaml('borrower', 'user_id')), data)

        # 借款人电话
        if re.search(cls.existed_borrower_tel_pattern, data):
            data = re.sub(cls.existed_borrower_tel_pattern,
                          cls.do_yaml_user.read_yaml('borrower', 'mobile_phone'), data)

        # 借款人密码
        if re.search(cls.existed_borrower_pwd_pattern, data):
            data = re.sub(cls.existed_borrower_pwd_pattern,
                          cls.do_yaml_user.read_yaml('borrower', 'pwd'), data)

        # 管理员电话
        if re.search(cls.existed_admin_tel_pattern, data):
            data = re.sub(cls.existed_admin_tel_pattern,
                          cls.do_yaml_user.read_yaml('admin', 'mobile_phone'), data)

        # 管理员密码
        if re.search(cls.existed_admin_pwd_pattern, data):
            data = re.sub(cls.existed_admin_pwd_pattern,
                          cls.do_yaml_user.read_yaml('admin', 'pwd'), data)

        # loan_id
        if re.search(cls.loan_id_pattern, data):
            loan_id = getattr(Parameterize, 'loan_id')
            data = re.sub(cls.loan_id_pattern, str(loan_id), data)

        # 不存在的loan_id
        if re.search(cls.not_existed_loan_id_pattern, data):
            # 创建数据库连接及游标对象
            do_mysql = HandleMysql()
            sql = "select id from loan order by id desc limit 0,1;"
            # 运行sql，得到一个字典
            res_max = do_mysql.run(sql, is_more=False)
            # 获取字典的值，转换为字符串，将原data进行参数化
            data = re.sub(cls.not_existed_loan_id_pattern,
                          str(res_max.get('id') + 1), data)
            # 关闭数据库游标对象、连接
            do_mysql.close()

        return data


if __name__ == '__main__':
    # one_str = '{"mobile_phone": "{not_existed_tel}","pwd": "123456","type":0,"reg_name":"cheer"}'
    # two_str = '{"mobile_phone": "","pwd": "123456789"}'
    # three_str = '{"mobile_phone": "{existed_tel}","pwd": "123456789"}'
    # one_str = '{"mobile_phone": "{investor_tel}","pwd": "{investor_pwd}"}'
    # two_str = '{"mobile_phone": "","pwd": "{investor_pwd}"}'
    # one_str = '{"mobile_phone": "{investor_tel}","pwd": "{investor_pwd}"}'
    two_str = '{"member_id": "{investor_id}","amount": 10}'
    # three_str = '{"member_id": {investor_id},"amount": 1}'
    # print(Parameterize.to_parameter(one_str))
    print(Parameterize.to_parameter(two_str))
    # print(Parameterize.to_parameter(three_str))
    # print(Parameterize.to_parameter(two_str))
    # print(Parameterize.to_parameter(three_str))
    pass
