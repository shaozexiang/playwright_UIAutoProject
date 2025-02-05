# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : slider.py
@Time : 2025/2/5 23:11
"""
from utils.locator_tools.base_page import BasePage, CustomLocator


class Slider:

    def __init__(self, page):
        self.base_page = BasePage(page)

    def slider_bar(self, index=None, win_loc: CustomLocator = None):
        loc = '//div[contains(@class, "el-slider")]//div[@class="el-slider__bar"]'

        bar_loc = self.base_page.locator(loc)
        if win_loc is not None:
            bar_loc = win_loc.locator(bar_loc)
        if index is not None:
            bar_loc = bar_loc.nth_element_locator(index)
        return bar_loc

    def slider_bar_btn(self):
        loc = '//div[contains(@class, "el-slider")]//div[@class="el-slider__button-wrapper"]'
        return self.base_page.locator(loc)

    def slider_input(self):
        loc = '//div[contains(@class, "el-slider")]//input[@class="el-input__inner"]'
        return self.base_page.locator(loc)

    def assert_slider_value(self, check_value, slider_loc: CustomLocator):
        """ 断言输入参数是否"""
        slider_loc.blur()
        expect_value = slider_loc.get_attribute("aria-valuenow")
        assert check_value == expect_value

