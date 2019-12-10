"""
============================
Author:cheer
# @time:2019-11-19 16:23
# @FileName: handle_path.py
# @Software: PyCharm
# @Cnblogs ：https://www.cnblogs.com/*****
============================
"""
import os

# # __file__
# one_path = os.path.abspath(__file__)
# # print(one_path)
# two_path = os.path.dirname(one_path)
# # print(two_path)
# three_path = os.path.dirname(two_path)
# print(three_path)

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 获取配置文件所在的目录
CONFIGS_DIR = os.path.join(BASE_DIR, 'configs')
# 获取配置文件所在的路径
CONFIG_FILE_PATH = os.path.join(CONFIGS_DIR, 'testcase.yaml')

# 获取日志文件所在的目录
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

# 获取生成测试报告的路径
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')

# 获取存放excel测试数据文件的路径
DATAS_DIR = os.path.join(BASE_DIR, 'datas')

# 存放用户个人信息配置文件路径
USER_INFO_DIR = os.path.join(CONFIGS_DIR, 'user_info.yaml')

# 获取测试用例类文件所在的目录
CASES_DIR = os.path.join(BASE_DIR, 'cases')

# print(USER_INFO_DIR)
# pass
