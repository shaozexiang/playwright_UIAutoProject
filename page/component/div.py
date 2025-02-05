# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : div.py
@Time : 2025/2/5 23:10
"""
from playwright.sync_api import Page

from utils.locator_tools.base_page import BasePage


class Div:
    def __init__(self, page: Page):
        self.base_page = BasePage(page)
        self.page = page

    def click_div_bar(self, name):
        """
        点击bar条，用于切换
        :return:
        """
        btn_tab_form = 'xpath=//div[@class="btn-tabs"]'
        self.base_page.locator(btn_tab_form).get_by_text(name, exact=True).click()

    def click_div_role_tab(self, name):
        self.base_page.get_by_role('tab', name=name).click()


    def assert_MulOptionsList(self, value):
        """
        断言多数据的情况
        :return:
        """
        loc = '//div[@class="el-select__tags"]'
        self.base_page.locator(loc).contain_text(value)

    def click_show_page_input(self, name=None):
        """ 如果只有一个触发跳转页面行为的按钮则不需要传入name属性"""
        loc = '//*[@class="txt el-tooltip__trigger el-tooltip__trigger"]'
        self.base_page.locator(loc).filter(has_text=name).click()

    def click_ClassBtn_btn(self, name):
        """ 点击class为btn的div标签"""
        # action CustomName elementType
        loc = '.btn'
        self.base_page.locator(loc).filter(has_text=name).click()

    def click_ClassInput_div(self, text=None) -> None:
        loc = '//div[@class="input-append"]'
        self.base_page.locator(loc).filter(has_text=text).click()

    def get_alert_locator(self):
        return self.base_page.get_by_role('alert')

