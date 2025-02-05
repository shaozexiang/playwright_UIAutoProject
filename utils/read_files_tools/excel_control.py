# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : excel_control.py
"""
import json
import xlrd
from xlutils.copy import copy
from utils.other_tools.get_file_path import ensure_path_sep

def get_excel_data(sheet_name: str, case_name: any) -> list:
    """
    读取 Excel 中的数据 并且将数据转化为yaml文件或者将数据存储到缓存当中便于之后可以直接测试接口的不同入参情况
    :param sheet_name: excel 中的 sheet 页的名称
    :param case_name: 测试用例名称
    :return:
    """
    res_list = []

    excel_dire = ensure_path_sep("\\data\\TestLogin.xls")
    work_book = xlrd.open_workbook(excel_dire, formatting_info=True)
    # 打开对应的子表
    work_sheet = work_book.sheet_by_name(sheet_name)
    # 读取一行
    idx = 0
    for one in work_sheet.col_values(0):
        # 运行需要运行的测试用例
        if case_name in one:
            req_body_data = work_sheet.cell(idx, 9).value
            resp_data = work_sheet.cell(idx, 11).value
            res_list.append((req_body_data, json.loads(resp_data)))
        idx += 1
    return res_list


def set_excel_data(sheet_index: int) -> tuple:
    """
    excel 写入
    :return:
    """
    excel_dire = '../data/TestLogin.xls'
    work_book = xlrd.open_workbook(excel_dire, formatting_info=True)
    work_book_new = copy(work_book)

    work_sheet_new = work_book_new.get_sheet(sheet_index)
    return work_book_new, work_sheet_new


if __name__ == '__main__':
    get_excel_data("异常用例", '111')

