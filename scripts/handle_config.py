"""
============================
Author:cheer
# @time:2019-11-06 21:55
# @FileName: handle_config.py
# @Software: PyCharm
# @Cnblogs ：https://www.cnblogs.com/*****
============================
"""
'''
封装读取.conf配置文件的类
'''
# 导入标准库 configparser
from configparser import ConfigParser

class HandleConfig(object):

     def config_read(self, filename):
         self.config = ConfigParser()
         self.config.read(filename, encoding='utf8')

     def get_value(self, section, option):
         """字符串"""
         return self.config.get(section, option)

     def get_value_int(self,  section, option):
         """
         整型
         :param section:
         :param option:
         :return:
         """
         return self.config.getint(section, option)

     def get_value_folat(self,  section, option):
         """
         浮点型
         :param section:
         :param option:
         :return:
         """
         return self.config.getfloat(section, option)

     def get_value_bool(self,  section, option):
         """
         布尔
         :param section:
         :param option:
         :return:
         """
         return self.config.getboolean(section, option)

     def get_value_other(self,  section, option):
         """
         布尔
         :param section:
         :param option:
         :return:
         """
         return eval(self.config.get(section, option))

     # 定义静态方法，不建议使用类方法，因为cls在这里用不到
     @staticmethod
     def config_write(datas, file):
         # 创建配置文件解析器对象,把config看作一个嵌套字典的空字典
         config = ConfigParser()
         # 把datas数据存入config
         for key in datas:
             config[key] = datas[key]
         # 写入配置文件
         with open(file, 'w', encoding='utf8') as f:
             config.write(f)

obj = HandleConfig()
obj.config_read('config_01.conf')

if __name__ == '__main__':
    print(obj.get_value('excel', 'data_name'))
