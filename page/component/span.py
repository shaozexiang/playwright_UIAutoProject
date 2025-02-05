# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : span.py
@Time : 2025/2/5 23:12
"""
from playwright.sync_api import Page

from utils.locator_tools.base_page import BasePage


class Span:
    def __init__(self, page: Page):
        self.page = page
        self.base_page = BasePage(page)

    def click_li_inner_span(self, text):
        """
        点击ul功能栏中，嵌套在在li的span
        :param text:
        :return:
        """
        loc = '//ul//li//span'
        ele = self.base_page.locator(loc).filter(has_text=text)
        ele.click()

    def click_div_inner_span(self, div_locator, text=None):
        if text is not None:
            self.base_page.locator(div_locator).locator(f"//span[text()='{text}']").click()
        else:
            loc_ele = self.base_page.locator(div_locator).locator(f"//span")
            loc_ele.click()


