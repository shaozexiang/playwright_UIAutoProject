# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : __init__.py.py
@Time : 2025/2/5 23:08
"""
"""
component里面是不同的组件对应的定位方式，
page的页面只需要调用component的组件就可以定位到相同类型的组件
"""
from playwright.sync_api import Page

from page.component.alert import Alert
from page.component.button import Button
from page.component.canvas import Canvas
from page.component.dialog import Dialog
from page.component.div import Div
from page.component.form import Form
from page.component.icon import Icon
from page.component.img import Img
from page.component.input import Input
from page.component.liItem import LiItem
from page.component.slider import Slider
from page.component.span import Span
from page.component.table import Table
from page.component.time_select import TimeSelect
from page.component.tree import TreeItem
from utils.locator_tools.base_page import BasePage


class Component:
    def __init__(self, page: Page):
        self.__page = page
        self.__base_page = BasePage(page)

    @property
    def table(self):
        return Table(self.__page)

    @property
    def input(self):
        return Input(self.__page)

    @property
    def button(self):
        return Button(self.__page)

    @property
    def LiItem(self):
        return LiItem(self.__page)

    @property
    def div(self):
        return Div(self.__page)

    @property
    def img(self):
        return Img(self.__page)

    @property
    def span(self):
        return Span(self.__page)

    @property
    def canvas(self):
        return Canvas(self.__page)

    @property
    def tree(self):
        return TreeItem(self.__page)

    @property
    def dialog(self):
        return Dialog(self.__page)

    @property
    def icon(self):
        return Icon(self.__page)

    @property
    def form(self):
        return Form(self.__page)

    @property
    def slider(self):
        return Slider(self.__page)

    @property
    def time(self):
        return TimeSelect(self.__page)

    @property
    def alert(self):
        return Alert(self.__page)

    @property
    def base_page(self):
        return BasePage(self.__page)

    def wait_for_request_finished(self):
        self.__base_page.wait_for_request_finished()

