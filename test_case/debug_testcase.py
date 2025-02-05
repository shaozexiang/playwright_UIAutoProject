# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : debug_testcase.py
"""
import asyncio
import os
import re
from asyncio import coroutine
from typing import Any

import pytest

from utils import ensure_path_sep

allure_tmp_path = ensure_path_sep("\\output\\report\\tmp")
allure_report_path = ensure_path_sep("\\output\\report\\html")
output_path = ensure_path_sep("\\test-result")


def allure_test(test_case_path, other_path=None):
    if other_path is not None:
        exec_testcase = ensure_path_sep(f"\\test_case\\{test_case_path}{other_path}")
    else:
        exec_testcase = ensure_path_sep("\\test_case\\" + test_case_path)
    arg_list = [
        '-s',
        f"{exec_testcase}",
        '-v',
        f'--alluredir={allure_tmp_path}',
        "--clean-alluredir",
        f"--output={output_path}"
    ]
    pytest.main(arg_list)
    os.system(f'allure generate {allure_tmp_path} -o {allure_report_path} --clean')
    os.system(f"allure serve {allure_tmp_path} -h 127.0.0.1 -p 9998")


def main():
    allure_test("\\test_main.py")


def main1():
    allure_test("assets_management\\test_hangar_management.py::TestHangarManagements")


def start_service():
    os.system(f'allure generate {allure_tmp_path} -o {allure_report_path} --clean')
    os.system(f"allure serve {allure_tmp_path} -h 127.0.0.1 -p 9999")


def pattern_test():
    pattern = "selector='(.*?)'"
    text = '''<Locator frame=<Frame name= url='http://10.0.20.22:17110/#/RouteManagement'> selector='xpath=//tbody//tr[0]//button >> internal:has-text="\\u9009\\u62e9\\u90e8\\u4ef6 "i >> div >> span >> nth=1 '>'''
    re_group = re.search(pattern, text).group(1)
    selector_list = re_group.split('>>')
    print_str = "定位元素为: "
    for selector_text in selector_list:
        if selector_text == selector_list[0]:
            print_str = print_str + "首层元素->" + selector_text
        elif 'internal' in selector_text:
            internal_text = selector_text.split(':')[1]
            if "\\u" in internal_text:
                internal_text = internal_text.encode('utf-8').decode('unicode_escape')
                print_str = print_str + "下一层定位元素->" + internal_text[:-1]
            else:
                print_str = print_str + "下一层定位元素->" + internal_text
        elif selector_text == selector_list[len(selector_list) - 1]:
            print_str = print_str + selector_text
        else:
            print_str = print_str + selector_text + "下一层定位元素->"
    print(print_str)


if __name__ == '__main__':
    start_service()

