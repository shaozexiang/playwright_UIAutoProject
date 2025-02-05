# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : tree.py
@Time : 2025/2/5 23:12
"""
from playwright.sync_api import Page

from utils.locator_tools.base_page import BasePage


class TreeItem:
    def __init__(self, page: Page):
        self.base_page = BasePage(page)
        self.page = page

    def select_contract_tree_option(self, tree_texts: list):
        """ 展开文件树并且选中文件树"""
        for text in tree_texts:
            if text == tree_texts[len(tree_texts) - 1]:
                self.base_page.get_by_role("treeitem", name=text).locator("span").click()
            else:
                self.base_page.get_by_role("treeitem", name=text).locator("i").click()

    def select_search_tree_option(self, text):
        """ 用于带有搜索功能的树"""
        loc = f'//div[@class="tree-item"]//span[@class="el-tree-node__label"]'
        self.base_page.locator(loc).filter(has_text=text).click()


