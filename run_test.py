"""
============================
Author:cheer
# @time:2019-11-06 19:53
# @FileName: run_test.py
# @Software: PyCharm
# @Cnblogs ：https://www.cnblogs.com/*****
============================
"""
'''
测试用例：TestCase
测试套件: TestSuite
测试运行程序：TestTextRunner
测试环境搭建和销毁：fixture
'''
import unittest
# 每执行一次生成一个报告，不覆盖原来的: 加 时间戳
import os
from datetime import datetime

from HTMLTestRunnerNew import HTMLTestRunner
# 导入配置封装模块
from scripts.handle_yaml import do_yaml
# 导入生成测试报告的路径
from scripts.handle_path import REPORTS_DIR, USER_INFO_DIR, CASES_DIR
from scripts.handle_user import generate_user_yaml

# 如果用户信息yaml文件不存在，则生成用户账号配置文件，否则不创建
if not os.path.exists(USER_INFO_DIR):
    generate_user_yaml()

# # 创建测试套件对象，导入用到的unittest的TestSuite
# suite = unittest.TestSuite()
# # 将测试用例添加到测试套件中：
# # 分为四种方法，使用ddt后这里使用将测试模块加入到测试套件中(导入测试用例类所在的模块）
# loader = unittest.TestLoader()
# suite.addTest(loader.loadTestsFromModule(test_01_register))
# suite.addTest(loader.loadTestsFromModule(test_02_login))

# 创建目录测试套件对象，使用unittest.defaultTestLoader.discover()
suite = unittest.defaultTestLoader.discover(CASES_DIR)

# 创建测试运行程序
# runner = unittest.TextTestRunner()

# 也可以生成测试报告，将HTMLTestRunnerNew.py放入python安装目录--lib下，并在该模块导入
report_name = do_yaml.read_yaml('report', 'report_name') + '_' \
              + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
report_name = os.path.join(REPORTS_DIR, report_name)

with open(report_name + '.html', 'wb') as f:
    runner = HTMLTestRunner(stream=f,
                            verbosity=2,
                            title=do_yaml.read_yaml('report', 'report_title'),
                            description=do_yaml.read_yaml('report', 'report_description'),
                            tester=do_yaml.read_yaml('report', 'report_tester'))
    # 将测试套件添加到测试运行程序
    runner.run(suite)
