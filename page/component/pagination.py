# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : pagination.py
@Time : 2025/2/5 23:11
"""
import typing
import warnings

import allure
from playwright.sync_api import Page

from utils.locator_tools.base_page import BasePage
from utils.other_tools.exceptions import ValueNotFoundError


class Pagination:
    """ 分页按钮"""

    def __init__(self, page):
        self.base_page = BasePage(page)
        self.page: Page = page

    @property
    def bg_pagination(self):
        return self.base_page.get_by_role("pagination")

    @allure.step("点击上一页按钮")
    def click_prev_btn(self):
        """ 点击上一页的按钮"""
        loc = '//button[contains(@class, "btn-prev")]'
        if self.base_page.locator(loc).element_is_disabled() is False:
            self.base_page.locator(loc).click()
        else:
            warnings.warn("点击上一页按钮的时候已经在第一页，所以不会再次触发点击行为", RuntimeWarning)

    @allure.step("点击下一页按钮")
    def click_next_btn(self):
        """ 点击上一页的按钮"""
        loc = '//button[contains(@class, "btn-next")]'
        if self.base_page.locator(loc).element_is_disabled() is False:
            self.base_page.locator(loc).click()
        else:
            warnings.warn("点击上一页按钮的时候已经在最后一页，所以不会再次触发点击行为", RuntimeWarning)

    # @todo
    @allure.step("点击特定页面 页面的页码为{text}")
    def click_pager(self, text: int):
        """ 点击跳转到特定"""
        loc = f'//ul[@class="el-pager"]/li[text()={text}]'
        public_loc = '//ul[@class="el-pager"]/li'
        active_page_loc = '//ul[@class="el-pager"]/li[@class="is-active number"]'
        if self.base_page.locator(loc).element_is_visible():
            self.base_page.locator(loc).click()
        else:
            max_pager = self.base_page.locator(public_loc).last_element_locator.text_content()
            active_pager = self.base_page.locator(active_page_loc).text_content()
            if int(max_pager) < text:
                raise ValueNotFoundError("点击的页码编号大于最大页码数，请重新输入")
            while self.page.locator(loc).is_visible() is False:
                if active_pager > text:
                    self.click_prev_btn()
                else:
                    self.click_next_btn()
                self.base_page.wait_for_timeout(50)
            self.base_page.locator(loc).click()

    def jump_pager_by_fill(self, number):
        """ 通过输入栏跳转到具体的页面"""
        loc = '//input[max]'
        loc_ele = self.bg_pagination.locator(loc)
        loc_ele.fill(str(number))
        loc_ele.press("Enter")

    def adjust_pagination_size(self):
        """ 调整分页大小"""
        loc = '//span[@class="el-pagination__sizes"]//input'
        self.bg_pagination.locator(loc).click()




