# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : button.py
@Time : 2025/2/5 23:09
"""
from playwright.sync_api import Page

from utils.locator_tools.base_page import BasePage


class Button:

    def __init__(self, page: Page):
        self.page = page
        self.button = BasePage(page)

    @property
    def confirm_btn_ele(self):
        return self.button.get_by_role('button', name="确 定")

    def click_import_btn(self, name):
        """
        点击导入按钮
        :param name: 导入按钮的名称
        :return:
        """
        pass

    def click_query_btn(self):
        self.button.get_by_role('button', name="查询").click()

    def click_confirm_btn(self):
        self.button.get_by_role('button', name="确 定").click()

    def click_submit_btn(self):
        self.button.get_by_role('button', name="提交").click()

    def click_cancel_btn(self):
        self.button.get_by_role('button', name="取 消").click()

    def click_search_btn(self):
        self.button.get_by_role('button', name="搜索").click()

    def click_dialog_btn(self, text):
        """ 特殊处理弹窗的控件按钮, 需要与页面分离开"""
        loc = '//div[@class="el-dialog__body"]//button'
        self.button.locator(loc).filter(has_text=text).click()

    def click_btn_by_name(self, name):
        self.button.get_by_role('button', name=name).click()

    def get_btn_by_name(self, name):
        return self.button.get_by_role('button', name=name)

    def click_insertConfirm_btn(self):
        self.button.get_by_role('button', name="确认添加").click()

