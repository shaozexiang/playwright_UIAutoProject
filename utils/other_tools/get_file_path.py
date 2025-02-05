# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : get_file_path.py
"""
import os.path
import pathlib
from typing import Text


def root_path():
    root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    return root


def ensure_path_sep(path) -> Text:
    if "/" in path:
        path = os.sep.join(path.split("/"))
    if "\\" in path:
        path = os.sep.join(path.split("\\"))
    return root_path() + path


def get_all_path(dir_path, yaml_data_switch=False) -> list:
    """
    通过文件夹路径遍历获取所有的文件路径
    :param dir_path:
    :return:
    """
    all_path = []
    for dir_path, dir_names, filenames in os.walk(dir_path):
        for filename in filenames:
            file_path = os.path.join(dir_path, filename)
            if ".pyc" not in file_path:
                if yaml_data_switch:
                    if 'yaml' in file_path or 'yml' in file_path:
                        all_path.append(file_path)
                else:
                    all_path.append(file_path)

    return all_path


def get_userHome_dir():
    home_dir = pathlib.Path.home()
    return home_dir


if __name__ == '__main__':
    # result = get_all_path(ensure_path_sep("\\file\\ui_upload_file\\test_import_airline.kmz"))
    result = get_all_path(ensure_path_sep("\\page"))
    print(result)
