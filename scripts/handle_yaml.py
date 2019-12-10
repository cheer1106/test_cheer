"""
============================
Author:cheer
# @time:2019-11-06 21:09
# @FileName: handle_yaml.py
# @Software: PyCharm
# @Cnblogs ：https://www.cnblogs.com/*****
============================
"""
'''
yaml 封装类
写入配置文件的原则：存放一些使用频繁，修改不频繁的数据
    几乎不需要改的内容，不需要写入配置文件，如log等级；
    频繁改的内容不需要写入配置文件，如表单名
    
定义静态方法：方法中用不到self，也用不到类属性，和这些没有关联的方法，定义为静态方法（为了封装的完整性；或者其他模块也会用到）
定义实例方法：方法中有用到self，把方法定义为实例方法
定义类方法：方法中用不到self，有用到类属性/类调用类方法的时候，定义为类方法
'''
# 导入第三方库
import yaml
# 导入拼接路径模块中的配置文件路径
from scripts.handle_path import CONFIG_FILE_PATH


class HandleYaml(object):
    """yaml读取/写入类"""

    # 也可以把__init__放到read_yaml方法中
    def __init__(self, filename):
        with open(filename, 'r', encoding='utf8') as file:
            self.data = yaml.load(file, Loader=yaml.FullLoader)

    def read_yaml(self, section, option):
        """
        获取配置数据
        :param section:
        :param option:
        :return:
        """
        return self.data[section][option]

    # 定义静态方法，不建议使用类方法，因为cls在这里用不到
    @staticmethod
    def write_yaml(file, datas):
        with open(file, 'w', encoding='utf8') as f:
            yaml.dump(datas, f, allow_unicode=True)


do_yaml = HandleYaml(CONFIG_FILE_PATH)

if __name__ == '__main__':
    print(do_yaml.read_yaml('excel', 'data_name'))
