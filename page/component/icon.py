# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : icon.py
@Time : 2025/2/5 23:11
"""
from playwright.sync_api import Page

from utils.locator_tools.base_page import BasePage


class Icon:
    def __init__(self, page: Page):
        self._base_page = BasePage(page)
        self._page = page

    def find_icon_btn_by_Class(self, IconClass, index):
        """
        返回icon图标
        :param IconClass:
        :param index:
        :return:
        """
        loc = f'//i[contains(@class,"{IconClass}")]'
        if self._page.locator(loc).count() > 1:
            return self._base_page.locator(loc).nth_element_locator(index)
        return self._base_page.locator(loc)

