# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : table.py
@Time : 2025/2/5 23:12
"""
import typing
from typing import Text

import allure
from playwright.sync_api import Page

from utils.locator_tools.base_page import BasePage


class Table:
    def __init__(self, page: Page):
        self.page = page
        self.base_page = BasePage(page)

    def get_table_lastCol(self, index, text):
        """

        :param index: 第几行
        :param text:  通过文本筛选控件
        :return:
        """
        loc = f'//tbody//tr[{index + 1}]//td[last()]//span'
        return self.base_page.locator(loc).filter(has_text=text)

    def click_table_lastCol(self, index, text):
        self.get_table_lastCol(index, text).click()

    @allure.step("勾选table表单中的第{index}行的数据")
    def select_table_option(self, index: typing.Union[int, list]):
        """
        勾选table列表的行的数据, 因为在table_option_object内采用的是索引的方式所以
        """
        index = index if isinstance(index, list) else [index]
        for i in index:
            self.table_option_object(index=i + 1).click()

    @allure.step("定位table表单中的第{index}行")
    def table_option_object(self, index, parent: str = None):
        loc = f'//tbody//tr[{index}]//td[1]//span//span'
        if parent is not None:
            return self.base_page.locator(parent).locator(loc)
        return self.base_page.locator(loc)

    @allure.step("选择table表单中的第{index}行，名称为{text}的按钮")
    def select_table_btn(self, index, text):
        """
        定位table表单中的某个button，输入名称需要注意空格
        """
        self.base_page.locator(f'xpath=//tbody//tr[{index}]//span').filter(has_text=text).click()

    @allure.step("定位table表单中的第{index}行，名称为{text}的列")
    def select_table_div(self, index, text):
        ele_loc = self.base_page.locator(f'xpath=//tbody//tr[{index}]//div').filter(has_text=text)
        return ele_loc

    def select_table_btn_span(self, index, text):
        self.base_page.locator(f'xpath=//tbody//tr[{index}]//button').filter(has_text=text).click()

    def select_dialog_table_option(self, index):
        parent_loc = '//div[contains(@class, "el-dialog")]'
        self.table_option_object(index, parent_loc).click()

    def get_table_locator_by_RCIndex(self, row_index, col_index):
        """ 通过行列的角标去获取到单元格对应的对象"""
        table_body = '//table[@class="el-table__body"]//tr[@class="el-table__row"]'
        # table_body = '//div[@class="tableBox"]//tr[@class="el-table__row"]'
        row_loc_ele = self.base_page.locator(table_body).nth_element_locator(row_index)
        return row_loc_ele.locator('//td//div[contains(@class,"cell")]').nth_element_locator(col_index)

