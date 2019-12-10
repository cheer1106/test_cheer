"""
============================
Author:cheer
# @time:2019-11-27 11:40
# @FileName: handle_user.py
# @Software: PyCharm
# @Cnblogs ：https://www.cnblogs.com/*****
============================
"""
'''
创建三个角色的用户：借款人、投资人、管理人账号
'''
from scripts.handle_request import HandleRequest
from scripts.handle_yaml import do_yaml
from scripts.handle_path import USER_INFO_DIR
from scripts.handle_mysql import HandleMysql


def create_new_user(reg_name, pwd='12345678', type=1):
    """
    创建一个新用户
    :param reg_name:
    :param pwd:
    :param type:
    :return:
    """
    # 创建session会话对象，用来发起请求
    do_request = HandleRequest()
    # 创建mysql对象
    do_mysql = HandleMysql()
    # 添加公共请求头
    do_request.add_headers(do_yaml.read_yaml('api', 'version'))

    # 注册请求的url
    register_url = do_yaml.read_yaml('api', 'prefix') + '/member/register'
    while True:
        # 随机生成一个未注册的手机号
        mobile_phone = do_mysql.create_not_exsited_mobile()
        # 创建一个请求体参数
        data = {
            'mobile_phone': mobile_phone,
            'pwd': pwd,
            'type': type,
            'reg_name': reg_name
        }
        # 调用注册接口，发起请求
        do_request.send(register_url, data=data)

        # 查询数据库用户ID的sql，同时进行了数据校验
        sql = do_yaml.read_yaml('mysql', 'select_user_id_sql')
        # 查询数据库，获取用户ID
        result = do_mysql.run(sql, args=[mobile_phone], is_more=False)
        # 判断是否存在，如果result为None，则用户不存在，if语句为真，用户创建成功，跳出循环
        if result:
            user_id = result['id']
            break

    # 构建用户信息为嵌套字典的字典
    user_info = {
        reg_name: {
            'user_id': user_id,
            'mobile_phone': mobile_phone,
            'pwd': pwd,
            'reg_name': reg_name}
    }

    # 关闭mysql对象
    do_mysql.close()
    # 关闭session会话对象
    do_request.close()

    return user_info


def generate_user_yaml():
    """
    生成三个用户
    :return:
    """
    # 创建一个空字典，
    user_data_dict = {}
    # 将新建的用户信息合并为一个嵌套字典的字典
    user_data_dict.update(create_new_user('admin', type=0))
    user_data_dict.update(create_new_user('investor'))
    user_data_dict.update(create_new_user('borrower'))
    # 写入到yaml文件
    do_yaml.write_yaml(USER_INFO_DIR, user_data_dict)


if __name__ == '__main__':
    generate_user_yaml()
