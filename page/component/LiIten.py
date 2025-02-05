# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : LiIten.py
@Time : 2025/2/5 23:11
"""
from playwright.sync_api import Page

from utils.locator_tools.base_page import BasePage


class LiItem:
    def __init__(self, page: Page):
        self.base_page = BasePage(page)
        self.page = page

    def click_second_item_bar(self, item_name):
        """
        点击菜单导航栏跳转到指定模块
        :param item_name:
        :return:
        """
        self.base_page.get_by_role("menuitem", name=item_name).click()

    def get_li_func_btn(self, text):
        loc = '//ul//li'
        return self.base_page.locator(loc).filter(has_text=text)

    def click_li_func_btn(self, text):
        """
        点击功能栏中li功能
        :param text:
        :return:
        """
        loc = '//ul//li'
        self.base_page.locator(loc).filter(has_text=text).click()

    def select_list_option(self, li_name, exact=False):
        """
        通过名称选择li列表的可选项 --- 匹配只能单选一个的情况, 这里会自动匹配div和span两种不同的标签
        不需要在li后面添加具体的参数
        例如：站点类型中可以选择光伏区站点or线路站点
        :param exact 准确匹配
        :return:
        """
        loc = '//div[@aria-hidden="false"]//ul//li'
        loc_ele = self.base_page.locator(loc).filter(has_text=str(li_name))
        if exact:
            loc = loc + f"//span[text()='{li_name}']"
            loc_ele = self.base_page.locator(loc)
        loc_ele.click()

    def close_MulOptions_list(self):
        mul_option_list_close_loc = '.el-select__tags'
        loc_ele = self.page.locator(mul_option_list_close_loc)
        if loc_ele.is_visible() is True:
            loc_ele.click()

    def select_list_option_number(self, number):
        """
        需要特殊处理下拉菜单为数字的情况，一般来说下拉菜单是不会出现重复项，所以使用全名称过滤会非常好用
        但是在数字的下拉菜单就可能出现2 12 22的情况，使用re过滤的方式就会出现错误
        :param number:
        :return:
        """
        loc = f'//div[@aria-hidden="false"]//ul//li//span[text()="{str(number)}"]'
        loc_ele = self.page.locator(loc)
        loc_ele.click()
        mul_option_list_close_loc = '.el-select__tags'
        loc_ele = self.page.locator(mul_option_list_close_loc)
        if loc_ele.is_visible() is True:
            loc_ele.click()

    def select_menu_inner_option(self, text, number=None):
        """ 选择菜单类型下的数据"""
        loc = '//div[@role="menu"]//ul/li'
        if number is not None:
            loc = f'//div[@role="menu"][{number}]//ul/li'
        self.base_page.locator(loc).filter(has_text=text).click()

    def select_list_mulOption(self, text):
        """ 选择多选框的下拉菜单"""
        loc = '//div[contains(@class, "is-multiple")]'
        self.base_page.locator(loc).locator("visible=true").locator(
            "//ul//li[@class='el-select-dropdown__item']").filter(text).click()


