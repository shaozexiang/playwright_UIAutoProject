# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : canvas.py
@Time : 2025/2/5 23:09
"""
from utils.locator_tools.base_page import BasePage


class Canvas:
    def __init__(self, page):
        self.page = BasePage(page)

    def get_canvas_locator(self):
        _canvas = self.page.locator('//canvas[@class="upper-canvas "]')
        return _canvas

    def get_canvas_size(self):
        _canvas = self.get_canvas_locator()
        return _canvas.bounding_box()

    def write_rectangle_in_canvas(self):
        x, y, width, height = self.get_canvas_size()
        self.page.mouse_move(x + 50, y + 50, step=50)
        self.page.mouse_down()
        self.page.mouse_move(x + width - 50, y + height - 50, step=50)
        self.page.mouse_up()
