# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : service_template.py
"""
import os.path
from datetime import datetime


def write_case(page_path, page):
    """ 通过page写入到service内"""
    with open(page_path, 'w', encoding="utf-8") as file:
        file.write(page)


def write_service_file(*, class_title, func_titles, func_params, page_path, import_path, class_ins, force):
    """

    :param func_params: 方法的参数
    :param import_path: page页面的导入路径
    :param page_path: service页面的路径
    :param class_title: 类名称
    :param func_titles: 方法名称
    :param class_ins: 类实例
    :param force: 是否强制写入
    :return:
    """
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 因为输出的是类内的方法所以需要先输出四个空格保证缩进量
    func_content = "    "
    func_content = func_content + "    ".join(
        [f"@allure.step('{func_title}')\n"
         f"    def {func_title}(self{',' + func_params.get(f'{func_title}') if len(func_params.get(f'{func_title}')) != 0 else func_params.get(f'{func_title}')}):\n"
         f"        self.{class_ins}.{func_title}({func_params.get(f'{func_title}')})\n"
         f"        \n" for func_title in func_titles]
    )
    page = f"""#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : {now}
import allure
from playwright.sync_api import Page
{import_path} import {class_title}, {class_title}Assert
from service.common_service import CommonService
from utils.locator_tools.base_page import BasePage

''' service层封装一个完整的业务操作'''


class {class_title}Service:
    def __init__(self, page: Page):
        self.{class_ins} = {class_title}(page)
        self.base_page = BasePage(page)
        self._base_assert = {class_title}Assert(page)
        self.com = CommonService(page)


{func_content}

"""
    if force:
        write_case(page_path, page)
    elif force is False:
        if not os.path.exists(page_path):
            write_case(page_path, page)
    else:
        raise KeyError("只支持传入bool类型参数")

