"""
============================
Author:cheer
# @time:2019-11-14 16:49
# @FileName: handle_request.py
# @Software: PyCharm
# @Cnblogs ：https://www.cnblogs.com/*****
============================
"""
import json
import requests


class HandleRequest(object):
    """
    处理请求
    """

    def __init__(self):
        # 使用session对象发起请求
        self.one_session = requests.Session()

    def add_headers(self, headers):
        """添加公共请求头"""
        # one_session.headers为会话对象的默认请求头
        self.one_session.headers.update(headers)

    def send(self, url, method="post", data=None, is_json=True, **kwargs):
        # 为了统一性 将data统一为字典
        # data可能为json格式的字符串，也可能为字典格式的字符串
        if isinstance(data, str):
            try:
                data = json.loads(data)  # json.loads()将json格式的字符串转换为python数据类型：字典
            except Exception as e:
                # print('使用日志收集器来记录日志')
                data = eval(data)  # 将字典格式的字符串转换为字典

        method = method.lower()  # 将传入的方法名统一为小写，也可以使用method.upper()转换为大写
        if method == 'get':  # 使用method.upper()的话，这里的get需要为大写
            # get方法的请求只能使用params接收data，因为没有请求体
            res = self.one_session.request(method, url, params=data, **kwargs)
        elif method in ('post', 'put', 'delete', 'patch'):  # 使用method.upper()的话，这里的方法名需要大写
            if is_json:  # 如果is_json = True（代表接口文档 中规定的请求体的传递格式）,那么为json格式传递
                res = self.one_session.request(method, url, json=data, **kwargs)
            else:
                res = self.one_session.request(method, url, data=data, **kwargs)
        else:
            res = None
            print(f'不支持【{method}】请求方法')
        return res

    def close(self):
        # 调用会话对象的close方法, 是释放资源, 还是可以发起请求的
        self.one_session.close()


if __name__ == '__main__':
    # 1.构造请求url
    login_url = 'http://api.lemonban.com/futureloan/member/login'
    recharge_url = 'http://api.lemonban.com/futureloan/member/recharge'

    # 2.创建登录请求参数
    # 请求头参数
    login_headers = {
        'X-Lemonban-Media-Type': 'lemonban.v2'
    }
    # 请求体参数
    login_param = {
        'mobile_phone': '15621867254',
        # "mobile_phone": "{existed_tel}",
        'pwd': '12345678'
    }

    do_request = HandleRequest()  # 创建HandleRequest对象
    do_request.add_headers(login_headers)  # 添加公共请求头

    # 执行登录
    login_res = do_request.send(login_url, data=login_param)
    json_datas = login_res.json()

    # 获取登录的token
    token = json_datas['data']['token_info']['token']
    # 获取用户的iD
    member_id = json_datas['data']['id']

    # 创建充值请求参数
    # # 请求头参数
    # recharge_headers = {
    #     'X-Lemonban-Media-Type': 'lemonban.v2',
    #     'Authorization': 'Bearer ' + token
    # }
    # 请求体参数
    recharge_param = {
        'member_id': member_id,
        'amount': '50000'
    }

    token_headers = {'Authorization': 'Bearer ' + token}
    do_request.add_headers(token_headers)  # 添加公共请求头

    # 执行充值
    recharge_res = do_request.send(recharge_url, data=recharge_param)
    pass