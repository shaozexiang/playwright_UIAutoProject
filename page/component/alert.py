# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : alert.py
@Time : 2025/2/5 23:08
"""
from utils.locator_tools.base_page import BasePage


class Alert:

    def __init__(self, page):
        self.base_page = BasePage(page)

    def success_alert(self, msg=None):
        """ 通过文本辅助定位元素"""
        loc = '//div[contains(@class, "el-message--success")]'
        return self.base_page.locator(loc).filter(msg)

    def warming_alert(self, msg=None):
        loc = '//div[contains(@class, "el-message--warning")]'
        return self.base_page.locator(loc).filter(msg)

    def info_alert(self, msg=None):
        loc = '//div[contains(@class, "el-message--info")]'
        return self.base_page.locator(loc).filter(msg)

    def error_alert(self, msg=None):
        loc = '//div[contains(@class, "el-message--error")]'
        return self.base_page.locator(loc).filter(msg)

    def expect_success_visible(self, msg=None):
        self.success_alert(msg).is_element_visible()

    def expect_error_visible(self, msg=None):
        self.success_alert(msg).is_element_visible()

    def expect_info_visible(self, msg=None):
        self.success_alert(msg).is_element_visible()

    def expect_warming_visible(self, msg=None):
        self.success_alert(msg).is_element_visible()

