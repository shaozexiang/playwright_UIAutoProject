# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : input.py
@Time : 2025/2/5 23:11
"""
import os
import time

from playwright.sync_api import Page

from utils import ensure_path_sep
from utils.locator_tools.base_page import BasePage
from utils.other_tools.exceptions import LocatorNotVisibleError

"""
通过具体的组件类型和playwright的定位方式进行定位
"""


class Input:
    def __init__(self, page: Page):
        self.base_page = BasePage(page)
        self.page = page

    def form_upload_file(self, file_name):
        """
        上传文件组件
        :param file_name: file目录下对应的组件名称
        :param multiple: 表示是否需要讲数据解决
        :return:
        """
        loc = '//input[@class="el-upload__input"]'
        multiple_loc = '//input[@multiple]'  # 用于判断是否支持上传整个文件
        if self.page.query_selector(loc) is not None:
            if self.page.query_selector(multiple_loc) is not None:
                self.base_page.locator(loc).upload_file(file_name, upload_type="multiple")
            else:
                self.base_page.locator(loc).upload_file(file_name, upload_type="dir")
        else:
            raise KeyError("表单上传文件失败，上传文件元素定位不唯一")

    def label_select_option(self, name):
        """
        label 关联的下拉菜单组件
        :param name:
        :return:
        """
        return self.base_page.get_by_label(name)

    def label_control_input(self, name):
        return self.base_page.get_by_label(name)

    def text_type_input(self, name=None):
        loc = '.el-input input[type="text"]'
        loc = '//*[@class="el-input"]//input[@type="text"]'
        return self.base_page.locator(loc).filter(has_text=name)

    # def number_type_input(self, *, index=None, text=None, parent_locator=None):
    #     """ equal_parent用来处理玩去拿一致的两个input，可以通过test-id标签解决或者获取上层元素解决"""
    #     loc = '//div[@role="group"]//div[text()="设置开始辅助点相对高度"]'
    #     loc = '//input[@type="number"]'
    #     if text is not None and parent_locator is not None:
    #         child_locator = self.base_page.locator(loc)
    #         parent_locator = child_locator.locator("..")
    #
    #         if parent_locator.filter(has_text=text).is_element_visible():
    #             return parent_locator.locator(loc)
    #
    #     return self.base_page.locator(loc).nth_element_locator(index)
    def number_type_input_by_name(self, *, text=None):
        """ 通过名称定位，这里的role=group可能不是一个常见的状态，需要注意"""
        loc = '//div[@role="group"]'
        loc_ele = self.base_page.locator(loc).filter(has_text=text)
        if loc_ele is not None:
            inner_loc = "//input[@type='number']"
            return loc_ele.locator(inner_loc)

    def div_inner_input(self, div_xpath, input_type=None):
        """ 外层div有唯一的定位的元素的情况"""
        if input_type is not None:
            return self.base_page.locator(div_xpath).locator(f'//input[@type={input_type}]')
        else:
            return self.base_page.locator(div_xpath).locator(f'//input')

    def click_dialog_input(self, input_type):
        """ 特殊处理dialog的弹窗情况"""
        dialog_loc = '//div[@role="dialog"]//*[contains(@class, "height-fix")]'
        input_loc = f'//input[@type="{input_type}"]'
        self.base_page.locator(dialog_loc).locator(input_loc).click()

    def get_dialog_input_element(self, dialog_width_size, placeholder_text=None):
        """ 粗略筛选dialog内的input标签
            需要注意，一般需要二级定位才能定位到需要的input标签
        """
        loc = f'//div[contains(@class, "el-dialog")]//div[@style="--el-dialog-width: {dialog_width_size};"]//input'
        if placeholder_text is not None:
            loc = f'//div[contains(@class, "el-dialog")]//div[@style="--el-dialog-width: {dialog_width_size};"]'
            return self.base_page.locator(loc).get_by_placeholder(placeholder_text)
        loc_ele = self.base_page.locator(loc)
        return loc_ele

    def fill_focusedInput(self, value):
        """
        使用 evaluate解析语句可能会导致无法触发输入事件，所以不推荐使用这种方式
        往聚焦的输入栏中输入数据
        :param value:
        :return:
        """
        focus_ele = self.page.evaluate('document.activeElement.tagName')
        if focus_ele.lower() == 'input':
            focus_id = self.page.evaluate(f'document.activeElement.id')
            self.base_page.locator(f"//input[@id='{focus_id}']").fill(value)
            self.page.wait_for_function(f'document.activeElement.value == "{value}"')


