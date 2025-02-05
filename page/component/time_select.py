# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : time_select.py
@Time : 2025/2/5 23:12
"""
from utils.locator_tools.base_page import BasePage


class TimeSelect:
    def __init__(self, page):
        self.base_page = BasePage(page)

    def select_time_number(self, day_num, last_month: bool = False):
        """
        点击当前月份的时间表选择时间
        :param day_num 选择日期对应的数字
        :param last_month 是否为上一个月的日期
        :return:
        """
        if last_month:
            self.base_page.locator(
                f'//div[@actualvisible="true"]//td[@class="prev-month"]//span[text()="{day_num}"]').click()
        else:
            self.base_page.locator(
                f'//div[@actualvisible="true"]//td[contains(@class,"available")]//span[text()="{day_num}"]').click()  # 包括了当前和其他本月时间的情况

    def click_time_input(self, nth_index):
        loc = '//form//div[@role="combobox"]//input'
        self.base_page.locator(loc).nth_element_locator(nth_index).click()

