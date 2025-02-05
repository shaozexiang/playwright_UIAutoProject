# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : service_automatic_control.py
"""
import ast
import os.path
import typing

import black

from utils import ensure_path_sep
from utils.other_tools.get_file_path import get_all_path
from utils.read_files_tools.service_template import write_service_file
from utils.read_files_tools.testcase_template import write_testcase_file


class AutomaticGeneration:
    def __init__(self):
        self.file_path = None
        self.target_path = None

    @property
    def get_component_path(self):
        return ensure_path_sep("\\page\\component")

    @property
    def get_page_path(self):
        page_path = ensure_path_sep("\\page")
        all_file_paths = get_all_path(page_path)
        for i in range(len(all_file_paths) - 1, -1, -1):
            if os.path.dirname(all_file_paths[i]) == self.get_component_path or "__init__.py" in all_file_paths[i]:
                all_file_paths.remove(all_file_paths[i])

        return all_file_paths

    def mk_dir(self, target_path):
        """ 创建文件夹"""
        dir_path = os.path.dirname(target_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)


class ServiceAutomaticGeneration(AutomaticGeneration):
    @property
    def get_service_path(self):
        """ 获取整个文件名称"""
        service_dir = ensure_path_sep("\\service")
        page_dir = ensure_path_sep("\\page")
        new_dir = os.path.dirname(self.file_path.replace(page_dir, service_dir))
        return new_dir + os.sep + self.split_path

    @property
    def read_pyFile_tree(self):
        py_file = self.file_path
        with open(py_file, 'r', encoding='utf-8') as file:
            file_content = file.read()
            return ast.parse(file_content)

    @property
    def split_path(self):
        """ 替换文件名称"""
        basename = os.path.basename(self.file_path)
        basename = basename.split("_page")[0]
        basename = basename.split('.')[0]
        new_name = basename.replace(basename, basename + "_service")
        return new_name + ".py"

    @property
    def get_import_path(self):
        # 获取缺少.py的名称
        import_name = self.file_path.split(".py")[0]
        import_name = import_name.split(os.sep + "page", 1)[-1]
        import_path = "from page" + ".".join(import_name.split(os.sep))
        return import_path

    @property
    def get_class_title(self) -> str:
        tree = self.read_pyFile_tree
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ClassDef):
                if "Assert" not in node.name:
                    return node.name

    @property
    def get_class_instance(self):
        class_title = self.get_class_title
        class_name = class_title.split("Page")[0].lower()
        return class_name + "_page"

    @property
    def get_func_title(self) -> list:
        tree = self.read_pyFile_tree
        functions = []
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ClassDef):
                if "Assert" not in node.name:
                    for child in node.body:
                        if isinstance(child, ast.FunctionDef):
                            if any(i in child.name[0:7] for i in
                                   ['insert', 'update', 'delete', 'query', 'export']) is True:
                                functions.append(child.name)
        return functions

    @property
    def get_func_params(self) -> dict:
        tree = self.read_pyFile_tree
        func_params = {}
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ClassDef):
                if "Assert" not in node.name:
                    for child in node.body:
                        if isinstance(child, ast.FunctionDef):
                            if any(i in child.name[0:7] for i in
                                   ['insert', 'update', 'delete', 'query', 'export']) is True:
                                args = child.args.args
                                temp = [arg.arg for arg in args if arg.arg != "self"]
                                func_params[child.name] = ",".join(temp)
        return func_params

    def service_automatic_generate(self, force):
        """ 自动生成service用例"""

        for page_path in self.get_page_path:
            # 创建文件
            self.file_path = page_path
            self.mk_dir(self.get_service_path)
            write_service_file(
                class_title=self.get_class_title,
                func_titles=self.get_func_title,
                func_params=self.get_func_params,
                page_path=self.get_service_path,
                class_ins=self.get_class_instance,
                import_path=self.get_import_path,
                force=force
            )
            os.system(f"black {self.get_service_path}")


class TestCaseAutomaticGeneration(AutomaticGeneration):

    @property
    def get_testcase_path(self):
        """ 获取整个文件名称"""
        testcase_dir = ensure_path_sep("\\test_case")
        page_dir = ensure_path_sep("\\page")
        new_dir = os.path.dirname(self.file_path.replace(page_dir, testcase_dir))
        return new_dir + os.sep + self.base_name

    @property
    def base_name(self):
        """ 文件名称"""
        basename = os.path.basename(self.file_path)
        basename = basename.split('.')[0]
        new_name = basename.replace(basename, "test_" + basename)
        return new_name + ".py"

    @property
    def import_path(self):
        import_name = self.file_path.split(".py")[0]
        import_name = import_name.split(os.sep + "page", 1)[-1]
        import_path = "from page" + ".".join(import_name.split(os.sep))
        return import_path

    def get_class_title(self):
        pass

    def case_automatic_generate(self, force):
        for page_path in self.get_page_path:
            self.file_path = page_path
            self.mk_dir(self.get_testcase_path)
            write_testcase_file(
                class_title="",
                testcase_page_path="",
                func_titles="",
                func_params="",
                import_path="",
                force="",
            )
            os.system(f"black {self.get_testcase_path}")


if __name__ == '__main__':
    automatic = ServiceAutomaticGeneration()
    automatic.file_path = r'D:\person\playwright_guangfu_project\playwright_guangfu\page\aa\aa_page.py'
    # result = automatic.get_func_params
    # print(result)
    automatic.service_automatic_generate(False)

