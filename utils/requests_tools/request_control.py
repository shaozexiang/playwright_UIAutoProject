# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : request_control.py
"""
import ast
import json
import os
import pathlib
import random
import time
import urllib
from typing import Tuple, Dict, Union, Text, List
from uuid import uuid4

import allure
import requests
import urllib3
from jsonpath import jsonpath
from requests import Response
from requests.adapters import HTTPAdapter, BaseAdapter
from requests_toolbelt import MultipartEncoder
from urllib3 import Retry

from utils.other_tools.get_file_path import ensure_path_sep
from utils.other_tools.models import RequestType
from utils.logging_tools.log_decorator import log_decorator
from utils.database_tools.mysql_control import AssertExecution
from utils.logging_tools.run_time_decorator import execution_duration
from utils.allure_tools.allure_step_handler import allure_step_no, allure_step, allure_attach
from utils.read_files_tools.regular_control import cache_regular, regular
from utils.requests_tools.set_current_request_cache import SetCurrentRequestCache
from utils.other_tools.models import TestCase, ResponseData
from utils import config

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class RequestControl:
    """ 封装请求 """

    def __init__(self, yaml_case):
        self.__session = None
        self.__yaml_case = TestCase(**yaml_case)

    def file_data_exit(
            self,
            file_data) -> None:
        """判断上传文件时，data参数是否存在"""
        # 兼容又要上传文件，又要上传其他类型参数
        try:
            _data = self.__yaml_case.data
            for key, value in ast.literal_eval(cache_regular(str(_data)))['data'].items():
                if "multipart/form-data" in str(self.__yaml_case.headers.values()):
                    file_data[key] = str(value)
                else:
                    file_data[key] = value
        except KeyError:
            ...

    @classmethod
    def multipart_data(
            cls,
            file_data: dict):
        """ 处理上传文件数据，创建一个multipartEncoder对象"""
        multipart = MultipartEncoder(
            # 此处发生修改，需要兼容上传多个文件的情况，所以上传的是列表、
            fields=file_data,  # 字典格式
            # boundary='--' + str(random.randint(int(1e28), int(1e29 - 1)))
            boundary=uuid4().hex
        )
        return multipart

    @classmethod
    def check_headers_str_null(
            cls,
            headers: Dict) -> Dict:
        """
        兼容用户未填写headers或者header值为int
        @return:
        """
        headers = ast.literal_eval(cache_regular(str(headers)))
        if headers is None:
            headers = {"headers": None}
        else:
            for key, value in headers.items():
                if not isinstance(value, str):
                    headers[key] = str(value)
        return headers

    @classmethod
    def multipart_in_headers(
            cls,
            request_data: Dict,
            header: Dict):
        """ 判断处理header为 Content-Type: multipart/form-data"""
        header = ast.literal_eval(cache_regular(str(header)))
        request_data = ast.literal_eval(cache_regular(str(request_data)))

        if header is None:
            header = {"headers": None}
        else:
            # 将header中的int转换成str
            for key, value in header.items():
                if not isinstance(value, str):
                    header[key] = str(value)
            if "multipart/form-data" in str(header.values()):
                # 判断请求参数不为空, 并且参数是字典类型
                if request_data and isinstance(request_data, dict):
                    # 当 Content-Type 为 "multipart/form-data"时，需要将数据类型转换成 str
                    for key, value in request_data.items():
                        if not isinstance(value, str):
                            request_data[key] = str(value)
                    # 这里是因为multipart/form-data 格式
                    # 在传递headers的Content-type参数时候需要携带有boundary的参数值
                    # 所以需要实例化MultipartEncoder对象
                    # 具体如下源码
                    #    @property
                    # def content_type(self):
                    #    return str(
                    #        'multipart/form-data; boundary={0}'.format(self.boundary_value)
                    #        )
                    request_data = MultipartEncoder(request_data)
                    header['Content-Type'] = request_data.content_type

        return request_data, header

    def file_prams_exit(self) -> Dict:
        """判断上传文件接口，文件参数是否存在"""
        try:
            params = self.__yaml_case.data['params']
        except KeyError:
            params = None
        return params

    @classmethod
    def text_encode(
            cls,
            text: Text) -> Text:
        """unicode 解码"""
        return text.encode("utf-8").decode("utf-8")

    @classmethod
    def response_elapsed_total_seconds(
            cls,
            res) -> float:
        """获取接口响应时长"""
        try:
            # 输出时间为毫秒
            return round(res.elapsed.total_seconds() * 1000, 2)
        except AttributeError:
            return 0.00

    def upload_file(
            self) -> Tuple:
        """
        判断处理上传文件
        :return:
        """
        # 处理上传多个文件的情况
        _files = []
        file_data = {}
        # 兼容又要上传文件，又要上传其他类型参数
        self.file_data_exit(file_data)
        _data = self.__yaml_case.data
        for key, value in ast.literal_eval(cache_regular(str(_data)))['file'].items():
            file_path = ensure_path_sep("\\file\\api_upload_file\\" + value)
            file_data[key] = (value, open(file_path, 'rb'), 'application/octet-stream')
            _files.append(file_data)
            # allure中展示该附件
            allure_attach(source=file_path)
        # 实例化一个上传文件的对象
        multipart = self.multipart_data(file_data)
        self.__yaml_case.headers['Content-Type'] = multipart.content_type
        # 获取拼接在url地址上的数据
        params_data = ast.literal_eval(cache_regular(str(self.file_prams_exit())))
        return multipart, params_data, self.__yaml_case

    def request_type_for_json(
            self,
            headers: Dict,
            method: Text,
            **kwargs) -> object:
        """ 判断请求类型为json格式 """
        _headers = self.check_headers_str_null(headers)
        _data = self.__yaml_case.data
        _url = self.__yaml_case.url
        res = self.__session.request(
            method=method,
            url=cache_regular(str(_url)),
            json=ast.literal_eval(cache_regular(str(_data))),
            data={},
            headers=_headers,
            verify=False,
            params=None,
            **kwargs
        )
        return res

    def request_type_for_none(
            self,
            headers: Dict,
            method: Text,
            **kwargs) -> object:
        """判断 requestType 为 None"""
        _headers = self.check_headers_str_null(headers)
        _url = self.__yaml_case.url
        res = self.__session.request(
            method=method,
            url=cache_regular(_url),
            data=None,
            headers=_headers,
            verify=False,
            params=None,
            **kwargs
        )
        return res

    def request_type_for_params(
            self,
            headers: Dict,
            method: Text,
            **kwargs) -> object:
        """判断 requestType 为 Params
        此代码非原先的代码
        """
        _headers = self.check_headers_str_null(headers)
        _url = self.__yaml_case.url
        _params = self.__yaml_case.data
        _url += '?'
        for key, value in _params.items():
            _url += key + "=" + str(value) + "&"
        _url = _url[:-1]
        res = self.__session.request(
            method=method,
            url=cache_regular(_url),
            data={},
            headers=_headers,
            verify=False,
            params=None,
            **kwargs
        )
        return res

    def request_type_for_file(
            self,
            method: Text,
            headers,
            **kwargs):
        """处理 requestType 为 file 类型"""
        multipart = self.upload_file()
        yaml_data = multipart[2]
        _headers = multipart[2].headers
        _headers = self.check_headers_str_null(_headers)
        res = self.__session.request(
            method=method,
            url=cache_regular(yaml_data.url),
            data=multipart[0],
            params=multipart[1],
            headers=ast.literal_eval(cache_regular(str(_headers))),
            verify=False,
            **kwargs
        )
        return res

    def request_type_for_data(
            self,
            headers: Dict,
            method: Text,
            **kwargs):
        """判断 requestType 为 data 类型"""
        data = self.__yaml_case.data
        _data, _headers = self.multipart_in_headers(
            ast.literal_eval(cache_regular(str(data))),
            headers
        )
        _url = self.__yaml_case.url
        res = self.__session.request(
            method=method,
            url=cache_regular(_url),
            data=_data,
            headers=_headers,
            verify=False,
            # proxies=proxies,
            **kwargs)

        return res

    @classmethod
    def get_export_api_filename(cls, res):
        """ 处理导出文件 """
        content_disposition = res.headers.get('content-disposition')
        filename_code = content_disposition.split("=")[-1]  # 分隔字符串，提取文件名
        filename = urllib.parse.unquote(filename_code)  # url解码
        urllib.parse.unquote(filename_code)
        return filename

    def request_type_for_export(
            self,
            headers: Dict,
            method: Text,
            **kwargs):
        """判断 requestType 为 export 导出类型"""
        _headers = self.check_headers_str_null(headers)
        _data = self.__yaml_case.data
        _url = self.__yaml_case.url
        res = self.__session.request(
            method=method,
            url=cache_regular(_url),
            json=ast.literal_eval(cache_regular(str(_data))),
            headers=_headers,
            verify=False,
            stream=False,
            data={},
            **kwargs)
        filepath = os.path.join(ensure_path_sep("\\file\\api_export_file"), self.get_export_api_filename(res))  # 拼接路径
        export_file = pathlib.Path(filepath)
        if export_file.exists():
            i = 0
            _temp = export_file
            while _temp.exists():
                i = i + 1
                _name = export_file.stem + f"({i})" + export_file.suffix
                _parent = export_file.parent
                _temp = _parent.joinpath(_name)
            export_file = _temp
        if res.status_code == 200:
            if res.text:  # 判断文件内容是否为空
                with open(export_file, 'wb') as file:
                    # iter_content循环读取信息写入，chunk_size设置文件大小
                    for chunk in res.iter_content(chunk_size=1):
                        file.write(chunk)
            else:
                print("文件为空")

        return res

    @classmethod
    def _request_body_handler(cls, data: Dict, request_type: Text) -> Union[None, Dict]:
        """处理请求参数 """
        if request_type.upper() == 'PARAMS':
            return None
        else:
            return data

    @classmethod
    def _sql_data_handler(cls, sql_data, res):
        """处理 sql 参数 """
        # 判断数据库开关，开启状态，则返回对应的数据
        if config.mysql_db.switch and sql_data is not None:
            sql_data = AssertExecution().assert_execution(
                sql=sql_data,
                resp=res.json()
            )

        else:
            sql_data = {"sql": None}
        return sql_data

    def _check_params(
            self,
            res,
            yaml_data: "TestCase",
    ) -> "ResponseData":
        data = ast.literal_eval(cache_regular(str(yaml_data.data)))
        _data = {
            "url": res.url,
            "is_run": yaml_data.is_run,
            "detail": yaml_data.detail,
            "response_data": res.text,
            # 这个用于日志专用，判断如果是get请求，直接打印url
            "request_body": self._request_body_handler(
                data, yaml_data.requestType
            ),
            "method": res.request.method,
            # 此处传入的参数为sql对应的参数而非setup_sql对应的参数
            "sql_data": self._sql_data_handler(sql_data=ast.literal_eval(cache_regular(str(yaml_data.sql))), res=res),
            "yaml_data": yaml_data,
            "headers": res.request.headers,
            "cookie": res.cookies,
            "assert_data": yaml_data.assert_data,
            "res_time": self.response_elapsed_total_seconds(res),
            "status_code": res.status_code,
            "teardown": yaml_data.teardown,
            "teardown_sql": yaml_data.teardown_sql,
            "body": data
        }
        # 抽离出通用模块，判断 http_request 方法中的一些数据校验
        return ResponseData(**_data)

    @classmethod
    @allure.step("发送api请求 - 请求地址为:{url}")
    def api_allure_step(
            cls,
            *,
            url: Text,
            headers: Text,
            method: Text,
            data: Text,
            assert_data: Text,
            res_time: Text,
            res: Text
    ) -> None:
        """ 在allure中记录请求数据 """
        allure_step_no(f"请求URL: {url}")
        allure_step_no(f"请求方式: {method}")
        allure_step("请求头: ", headers)
        allure_step("请求数据: ", data)
        allure_step("预期数据: ", assert_data)
        _res_time = res_time
        allure_step_no(f"响应耗时(ms): {str(_res_time)}")
        allure_step("响应结果: ", res)

    def fetch_with_retry(self, requests_type_mapping, retires=5, delay=2, **kwargs):
        for attempt in range(1, retires):
            res: Response = requests_type_mapping.get(self.__yaml_case.requestType)(
                headers=self.__yaml_case.headers,
                method=self.__yaml_case.method,
                **kwargs
            )
            json_data = res.json()
            if ast.literal_eval(str(json_data['code'])) == 200:
                return res
            elif "已存在" in res.text:
                return res
            elif "过快" in res.text:
                time.sleep(delay * attempt)
                continue
            else:
                return res

    @log_decorator(True)
    @execution_duration(3000)
    # @encryption("md5")
    def http_request(
            self,
            dependent_switch=True,
            **kwargs
    ):
        """
        请求封装
        :param dependent_switch: 多业务逻辑标志位
        :param kwargs:
        :return:
        """
        from utils.requests_tools.dependent_case import DependentCase
        requests_type_mapping = {
            RequestType.JSON.value: self.request_type_for_json,
            RequestType.NONE.value: self.request_type_for_none,
            RequestType.PARAMS.value: self.request_type_for_params,
            RequestType.FILE.value: self.request_type_for_file,
            RequestType.DATA.value: self.request_type_for_data,
            RequestType.EXPORT.value: self.request_type_for_export
        }

        is_run = ast.literal_eval(cache_regular(str(self.__yaml_case.is_run)))
        # 判断用例是否执行
        if is_run is True or is_run is None:
            # 处理多业务逻辑
            if dependent_switch is True:
                DependentCase(self.__yaml_case).get_dependent_data()
            # res = requests_type_mapping.get(self.__yaml_case.requestType)(
            #     headers=self.__yaml_case.headers,
            #     method=self.__yaml_case.method,
            #     **kwargs
            # )
            self.__session = requests.session()
            res = self.fetch_with_retry(requests_type_mapping, **kwargs)
            res.close()
            if self.__yaml_case.sleep is not None:
                time.sleep(self.__yaml_case.sleep)

            _res_data = self._check_params(
                res=res,
                yaml_data=self.__yaml_case)
            self.api_allure_step(
                url=_res_data.url,
                headers=str(_res_data.headers),
                method=_res_data.method,
                data=str(_res_data.body),
                assert_data=str(_res_data.assert_data),
                res_time=str(_res_data.res_time),
                res=_res_data.response_data
            )
            if res.json()['code'] == 500:
                raise KeyError("接口上传数据已存在，请检查是否出现冲突数据")
            # 将当前请求数据存入缓存中
            SetCurrentRequestCache(
                current_request_set_cache=self.__yaml_case.current_request_set_cache,
                request_data=self.__yaml_case.data,
                response_data=res
            ).set_caches_main()

            return _res_data

