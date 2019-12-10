"""
============================
Author:cheer
# @time:2019-11-06 19:43
# @FileName: test_case.py
# @Software: PyCharm
# @Cnblogs ：https://www.cnblogs.com/*****
============================
"""
'''
投资测试用例类
'''
# 导入标准模块
import unittest
import json

# 导入自己封装的读数据模块
from scripts.handle_excel import ReadExcel
# ddt驱动，导入ddt
from libs.ddt import ddt, data
# 导入日志收集器
from scripts.handle_log import do_log
# 导入request模块
from scripts.handle_request import HandleRequest
# 导入参数化类
from scripts.handle_parameterize import Parameterize
# 用来生成用户配置文件
from scripts.handle_yaml import do_yaml
from scripts.handle_mysql import HandleMysql


# 封装测试用例类,继承于unittest的TestCase
@ddt
class TestInvest(unittest.TestCase):
    excel = ReadExcel('invest')
    cases = excel.read_data()

    # 所有用例执行之前创建session会话对象，设置公共请求头
    @classmethod
    def setUpClass(cls):
        # 创建session对象
        cls.do_request = HandleRequest()
        # 添加到配置文件并设置公共请求头
        cls.do_request.add_headers(do_yaml.read_yaml('api', 'version'))
        # 创建mysql数据连接，用来做数据校验
        cls.do_mysql = HandleMysql()

    @classmethod
    def tearDownClass(cls):
        # 测试用例类中的所有用例执行结束后，关闭session对象
        cls.do_request.close()
        # 关闭mysql数据连接
        cls.do_mysql.close()

    # 实例方法（代表测试用例）,必须以test开头
    @data(*cases)
    def test_invest(self, case):
        # 回写结果的row
        row = case.case_id + 1

        # 从excel中读取数据，准备请求参数
        # 拼接完整的url
        new_url = do_yaml.read_yaml('api', 'prefix') + case.url
        # 参数化获取发起请求的用例数据
        new_data = Parameterize.to_parameter(case.data)

        # 对象调用类属性向服务器发起请求
        res = self.do_request.send(new_url, method=case.method, data=new_data)

        # 将响应报文中的json格式数据（响应体）转换为字典
        actual_value = res.json()

        # 获取标ID

        # # 获取token
        # if case.case_id == 2:
        #     token_headers = {'Authorization': 'Bearer ' + actual_value['data']['token_info']['token']}
        #     self.do_request.add_headers(token_headers)

        # 从excel中获取excepted
        excepted_result = case.excepted

        # 获取title
        msg = case.title

        # 从配置文件中读取断言结果：成功
        success_result = do_yaml.read_yaml('excel', 'success_result')
        # 从配置文件中读取断言结果：失败
        fail_result = do_yaml.read_yaml('excel', 'fail_result')

        # 比较预期和实际结果
        # 捕获异常，回写结果，打印日志，并主动抛出异常
        try:
            self.assertEqual(actual_value.get('code'), excepted_result, msg=msg)
        except AssertionError as e:
            # 回写断言结果
            self.excel.write_result(row,
                                    do_yaml.read_yaml('excel', 'result_col'),
                                    fail_result)
            # 将异常内容写入日志
            # do_log.error(f'{msg}，执行结果为：{fail_result},具体异常为：{e}\n')
            do_log.error({e})
            # 主动抛出异常
            raise e
        else:
            # 获取token(也可以在发送请求后通过case_id 来判断登录用例从而获取token)
            # 也可以使用成员运算：if 'token' in res.text:
            if actual_value.get('data'):
                if actual_value.get('data').get('token_info'):
                    token_headers = {'Authorization': 'Bearer ' + actual_value['data']['token_info']['token']}
                    self.do_request.add_headers(token_headers)

            # 获取loan_id  (更方便的是直接从响应报文中获取loan_id)
            case_sql = case.case_sql
            if case_sql:
                # 也可以使用成员运算来判断
                if 'loan_id_sql' in case_sql:
                    case_sql = json.loads(case_sql, encoding='utf8').get('loan_id_sql')
                    # 借款人ID参数化
                    case_sql = Parameterize.to_parameter(case_sql)
                    # 查询数据库中该借款人对应的最新的loan_id
                    loan_id_dict = self.do_mysql.run(case_sql, is_more=False)
                    # 从结果字典中取loan_id
                    loan_id = loan_id_dict.get('id')
                    # 反射机制动态设置类属性，然后进行参数化，使得之后的用例可以取得loan_id（接口依赖）
                    setattr(Parameterize, 'loan_id', loan_id)

            # 回写断言结果
            self.excel.write_result(row,
                                    do_yaml.read_yaml('excel', 'result_col'),
                                    success_result)
            # 打印日志
            do_log.info(f'{msg}，执行结果为：{success_result}')
        finally:
            # 将返回的响应体写入excel
            self.excel.write_result(row,
                                    do_yaml.read_yaml('excel', 'actual_col'),
                                    res.text)


if __name__ == '__main__':
    unittest.main()
