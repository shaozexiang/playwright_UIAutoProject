# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : testcase_template.py
"""
import os.path
from datetime import datetime


def write_case(page_path, page):
    """ 通过page写入到service内"""
    with open(page_path, 'w', encoding="utf-8") as file:
        file.write(page)


def write_testcase_file(*, class_title, testcase_page_path, func_titles, func_params, import_path, force):
    """

    :param func_params: 方法参数
    :param testcase_page_path: testcase对应的路径
    :param import_path: service页面的导入路径
    :param class_title: service类名称
    :param func_titles: 方法名称
    :param force: 是否强制写入
    :return:
    """
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    func_content = "    "
    func_content = func_content + "    ".join(
        [
            f"@allure.story('{func_title}')\n"
            f"#def {func_title}(self, keep_login, page, clear_data)\n"
            f"    def {func_title}(self, connect_exists_browser):\n"
            f"        service = {class_title}(connect_exists_browser)\n\n"
            f"        service.{func_title}({func_params})" for func_title in func_titles
        ]
    )
    page = f"""#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : {now}
import pytest
import allure
from playwright.sync_api import Page
{import_path} import {class_title}
from utils.cache_process.cache_control import CacheHandler
from utils.requests_tools.api_request_control import send_request
from utils.time_tools.time_control import get_today_day


@pytest.fixture
def clear_data(page):
    yield
    send_request("")

@allure.epic("{class_title}")
@allure.feature("{class_title}")
class {class_title}:
    {func_content}

"""
    if force:
        write_case(testcase_page_path, page)
    elif force is False:
        if not os.path.exists(testcase_page_path):
            write_case(testcase_page_path, page)
    else:
        raise KeyError("只支持传入bool类型参数")

