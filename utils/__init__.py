# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : __init__.py.py
"""
from utils.read_files_tools.yaml_control import GetYamlData
from utils.other_tools.get_file_path import ensure_path_sep
from utils.other_tools.models import Config

_data = GetYamlData(ensure_path_sep("\\config\\config.yaml")).get_yaml_data()
config = Config(**_data)

