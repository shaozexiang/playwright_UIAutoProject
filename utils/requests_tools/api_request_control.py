# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : api_request_control.py
"""
from typing import Union, List

from utils.assertion.assert_control import Assert
from utils.read_files_tools.get_yaml_data_analysis import GetTestCase
from utils.read_files_tools.regular_control import regular
from utils.requests_tools.request_control import RequestControl


def send_request(case_id: Union[list, str]):
    """ 封装发送请求方法"""
    if isinstance(case_id, str):
        testcase_data = GetTestCase.case_data([case_id])[0]
        re_data = eval(regular(str(testcase_data)))
        res = RequestControl(re_data).http_request()
        Assert(assert_data=testcase_data['assert_data'],
               sql_data=res.sql_data,
               request_data=res.body,
               response_data=res.response_data,
               status_code=res.status_code).assert_type_handle()
    else:
        testcase_data = GetTestCase.case_data(case_id)
        for i in testcase_data:
            re_data = eval(regular(str(i)))
            res = RequestControl(re_data).http_request()
            Assert(assert_data=i['assert_data'],
                   sql_data=res.sql_data,
                   request_data=res.body,
                   response_data=res.response_data,
                   status_code=res.status_code).assert_type_handle()

