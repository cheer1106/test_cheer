"""
============================
Author:cheer
# @time:2019-11-06 20:02
# @FileName: handle_log.py
# @Software: PyCharm
# @Cnblogs ：https://www.cnblogs.com/*****
============================
"""
'''
封装日志类：导入logging 
'''
import logging
import os
# 导入配置文件封装模块
from scripts.handle_yaml import do_yaml
# 导入拼接路径模块中的配置文件路径
from scripts.handle_path import LOGS_DIR


class HandleLogger(object):
    @classmethod
    def handle_logger(cls):
        # 创建一个日志收集器
        # my_log = logging.getLogger('my_log')
        my_log = logging.getLogger(do_yaml.read_yaml('log', 'log_name'))
        # 设置收集等级
        # my_log.setLevel('DEBUG')
        my_log.setLevel(do_yaml.read_yaml('log', 'in_level'))

        # 设置输出格式
        # formater = logging.Formatter('%(asctime)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s')
        formater = logging.Formatter(do_yaml.read_yaml('log', 'formater_content'))
        # 输出到控制台
        sh = logging.StreamHandler()
        # 设置输出等级
        # sh.setLevel("WARNING")
        sh.setLevel(do_yaml.read_yaml('log', 'out_level'))
        # 将输出格式设置到控制台
        sh.setFormatter(formater)
        # 将输出终端添加到收集器
        my_log.addHandler(sh)

        # 输出到日志文件
        # fh = logging.FileHandler('log_1106.log', encoding='utf8')
        # fh = logging.FileHandler(do_yaml.read_yaml('log', 'log_file'), encoding='utf8')
        fh = logging.FileHandler(os.path.join(LOGS_DIR, do_yaml.read_yaml('log', 'log_file')),
                                 encoding='utf8')
        # 设置输出等级
        # fh.setLevel("WARNING")
        fh.setLevel(do_yaml.read_yaml('log', 'out_level'))
        # 将输出格式设置到日志文件
        fh.setFormatter(formater)
        # 将输出终端添加到收集器
        my_log.addHandler(fh)

        # 返回收集器
        return my_log


do_log = HandleLogger.handle_logger()

# if __name__ == '__main__':
#     do_log.debug('debug')
#     do_log.warning('warning')
