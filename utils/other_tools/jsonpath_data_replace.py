# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : jsonpath_data_replace.py
"""
from typing import Text


def jsonpath_replace(change_data, key_name, data_switch=None):
    """处理jsonpath数据
    :param: data_switch
    """
    _new_data = key_name + ''
    for i in change_data:
        if i == '$':
            continue
        elif i[0] == '[' and i[-1] == ']':
            _new_data += "[" + i[1:-1] + "]"
        elif data_switch is None:
            if i == "data":
                _new_data += '.data'
            elif i == "url":
                _new_data += '.url'
        else:
            _new_data += '[' + '"' + i + '"' + "]"
    return _new_data


if __name__ == '__main__':
    result = jsonpath_replace(change_data=['$', 'url'], key_name='self.__yaml_case', data_switch=None)
    print(result)

