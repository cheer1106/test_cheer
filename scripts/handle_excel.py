"""
============================
Author:cheer
# @time:2019-11-06 10:35
# @FileName: handle_excel.py
# @Software: PyCharm
# @Cnblogs ：https://www.cnblogs.com/*****
============================
"""
'''
从excel中读取数据
'''
# 第三方库
import openpyxl
import os

# 导入拼接路径模块中的测试数据存放的路径
from scripts.handle_path import DATAS_DIR
# 导入日志封装文件
from scripts.handle_yaml import do_yaml


# 用来存储数据对象
class CaseData(object):
    pass


class ReadExcel(object):
    # 将读取的工作簿和表单定义为实例属性
    def __init__(self, sheetname, filename=None):
        if filename is None:
            self.filename = os.path.join(DATAS_DIR, do_yaml.read_yaml('excel', 'data_name'))
        else:
            self.filename = filename
        self.sheetname = sheetname

    # 打开工作簿和对象，需要使用openpyxl:主要针对.xlsx的格式的excel进行读取和编辑
    def open(self):
        self.wb = openpyxl.load_workbook(self.filename)  # 动态定义实例属性，wb是工作簿对象
        self.sh = self.wb[self.sheetname]  # 动态定义实例属性

    # 读取数据
    def read_data(self):
        # 打开工作簿和表单
        self.open()
        # 读取数据
        # 按行读取所有的格子对象
        rows = list(self.sh.rows)
        # print(rows)
        title = []
        # 遍历获取表头
        for t in rows[0]:
            title.append(t.value)
        # print(title)

        # 遍历获取数据
        # 将最终数据对象存入列表中
        cases = []
        # 遍历除表头外的所有数据行
        for r in rows[1:]:
            # 将每一行数据存入列表中
            data_row = []
            # 遍历单行数据，获取每个格子对象的值，存入列表
            for data in r:
                data_row.append(data.value)
            # 将表头和单行数据聚合打包,返回列表嵌套对象的形式
            case = CaseData()
            # print(list(zip(title, data_row)))
            for data_case in zip(title, data_row):
                # 设置对象的属性值，属性名
                setattr(case, data_case[0], data_case[1])
            cases.append(case)
            self.wb.close()
        return cases

    # 回写结果
    def write_result(self, row, column, value):
        # 打开工作簿和表单
        self.open()
        # 写入数据
        self.sh.cell(row=row, column=column, value=value)
        # 保存
        self.wb.save(self.filename)
        # 关闭工作簿
        self.wb.close()

if __name__ == '__main__':
    obj = ReadExcel('register')
    print(obj.read_data())