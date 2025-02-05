# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : dialog.py
@Time : 2025/2/5 23:09
"""
from utils.locator_tools.base_page import BasePage


class Dialog:
    def __init__(self, page):
        self.page = page
        self._base_page = BasePage(page)
        self.__dialog_windows_loc = self._base_page.locator('//div[@class="el-overlay"]')

    @property
    def dialog_windows_loc(self):
        return self.__dialog_windows_loc.locator("visible=true")

    def dialog_label_control_input(self, name):
        """获取dialog 内的输入标签对应的对象"""
        from page.component import Component
        _input = Component(self.page).input
        return self.dialog_windows_loc.locator(_input.label_control_input(name))

    def dialog_item_input(self, text, index):
        """ 通过text找到form内的item，再通过index索引值去找到需要输入的是哪个input标签"""
        from page.component import Component
        _form = Component(self.page).form
        # return self.dialog_windows_loc.locator(_form.form_item_input(text, index))
        return _form.form_item_input(text, index)

    def dialog_item_content(self, text):
        from page.component import Component
        _form = Component(self.page).form
        return _form.form_item_content(text)
