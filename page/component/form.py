# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : form.py
@Time : 2025/2/5 23:10
"""
from page.component import Dialog
from utils.locator_tools.base_page import BasePage


class Form:
    def __init__(self, page):
        self.base_page = BasePage(page)
        self.dialog = Dialog(page)

    def form_item_content(self, text):
        """ 通过名称定位form表单内的items"""
        loc = '//div[contains(@class, "el-form-item")]'
        item_input_loc = '//div[@class="el-form-item__content"]'
        return self.base_page.locator(loc).filter(has_text=text).locator(item_input_loc)

    # def form_classLabel(self, text):
    #     """ form 表单内的label标签伪类"""
    #     loc = '.el_form-item_label'
    #     return self.base_page.locator(loc).filter(has_text=text)

    def form_item_input(self, text, index):
        """ 表单内的label标签伪类里面的输入栏"""
        loc = '//input[@class="el-input__inner"]'
        content = self.form_item_content(text)
        return content.locator(loc).nth_element_locator(index)


