# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : models.py
"""
import types
# 标准库导入
from enum import Enum, unique  # python 3.x版本才能使用
from typing import Text, Union, Dict, Optional, List, Any
from dataclasses import dataclass

from pydantic import BaseModel


def load_module_functions(module) -> dict:
    """
    获取模块中的所有方法
    :param module: 模块名称
    :return:
    """
    module_functions = {}
    for key, value in vars(module).items():
        if isinstance(value, types.FunctionType):
            module_functions[key] = value
    return module_functions


class TestCase(BaseModel):
    url: Text
    method: Text
    detail: Text
    # assert_data: Union[Dict, Text] = Field(..., alias="assert")
    assert_data: Union[Dict, Text]
    headers: Union[None, Dict, Text] = {}
    requestType: Text
    is_run: Union[None, bool] = None
    data: Any = None
    only_dependence: bool = False
    dependence_case: Union[None, bool] = False
    dependence_case_data: Optional[Union[None, List["DependentCaseData"], Text, List]] = None
    sql: Union[List, None] = None
    setup_sql: Union[List, None] = None
    status_code: Optional[int] = None
    teardown_sql: Optional[List] = None
    teardown: Union[List["TearDown"], None, List] = None
    current_request_set_cache: Optional[List["CurrentRequestSetCache"]]
    sleep: Optional[Union[int, float]]


class DependentData(BaseModel):
    dependent_type: Text
    jsonpath: Text
    set_cache: Optional[Text]
    replace_key: Optional[Text]
    assert_data: Union[None, Dict] = None


class DependentCaseData(BaseModel):
    case_id: Text
    dependent_data: Union[None, List[DependentData]] = None


class TearDown(BaseModel):
    case_id: Text
    param_prepare: Optional[List["ParamPrepare"]]
    send_request: Optional[List["SendRequest"]]


class CurrentRequestSetCache(BaseModel):
    type: Text
    jsonpath: Text
    name: Text


class ParamPrepare(BaseModel):
    dependent_type: Text
    jsonpath: Text
    set_cache: Text
    assert_type: bool = False
    assert_data: Union[None, Dict] = None


class SendRequest(BaseModel):
    dependent_type: Text
    jsonpath: Optional[Text]
    # 缓存名称
    cache_data: Optional[Text]
    # 设置缓存关键词
    set_cache: Optional[Text]
    # 替换表达式
    replace_key: Optional[Text]


class Assert(BaseModel):
    jsonpath: Text
    type: Text
    value: Any
    AssertType: Union[None, Text] = None
    message: str


class DingTalk(BaseModel):
    webhook: Union[Text, None]
    secret: Union[Text, None]


class MySqlDB(BaseModel):
    switch: bool = False
    host: Union[Text, None] = None
    user: Union[Text, None] = None
    password: Union[Text, None] = None
    port: Union[int, None] = 3306


class Webhook(BaseModel):
    # 飞书 or 企微
    webhook: Union[Text, None]


class Email(BaseModel):
    send_user: Union[Text, None]
    email_host: Union[Text, None]
    stamp_key: Union[Text, None]
    # 收件人
    send_list: Union[Text, None]


@unique
class AssertMethod(Enum):
    """断言类型"""
    equals = "=="
    less_than = "lt"
    less_than_or_equals = "le"
    greater_than = "gt"
    greater_than_or_equals = "ge"
    not_equals = "not_eq"
    string_equals = "str_eq"
    length_equals = "len_eq"
    length_greater_than = "len_gt"
    length_greater_than_or_equals = 'len_ge'
    length_less_than = "len_lt"
    length_less_than_or_equals = 'len_le'
    contains = "contains"
    contained_by = 'contained_by'
    startswith = 'startswith'
    endswith = 'endswith'
    int_equal = 'int_eq'


class NotificationType(Enum):
    """ 自动化通知方式 """
    DEFAULT = '0'
    DING_TALK = '1'
    WECHAT = '2'
    EMAIL = '3'
    FEI_SHU = '4'


@unique  # 枚举类装饰器，确保只有一个名称绑定到任何一个值。
class AllureAttachmentType(Enum):
    """
    allure 报告的文件类型枚举
    """
    TEXT = "txt"
    CSV = "csv"
    TSV = "tsv"
    URI_LIST = "uri"

    HTML = "html"
    XML = "xml"
    JSON = "json"
    YAML = "yaml"
    PCAP = "pcap"

    PNG = "png"
    JPG = "jpg"
    SVG = "svg"
    GIF = "gif"
    BMP = "bmp"
    TIFF = "tiff"

    MP4 = "mp4"
    OGG = "ogg"
    WEBM = "webm"

    PDF = "pdf"


class RequestType(Enum):
    """
    request请求发送，请求参数的数据类型
    """
    JSON = "JSON"
    PARAMS = "PARAMS"
    DATA = "DATA"
    FILE = 'FILE'
    EXPORT = "EXPORT"
    NONE = "NONE"


class Method(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTION = "OPTION"


class TestCaseEnum(Enum):
    URL = ("url", True)
    HOST = ("host", True)
    METHOD = ("method", True)
    DETAIL = ("detail", True)
    IS_RUN = ("is_run", True)
    HEADERS = ("headers", True)
    REQUEST_TYPE = ("requestType", True)
    DATA = ("data", True)
    DE_CASE = ("dependence_case", True)
    DE_CASE_DATA = ("dependence_case_data", False)
    CURRENT_RE_SET_CACHE = ("current_request_set_cache", False)
    SQL = ("sql", False)
    ASSERT_DATA = ("assert", True)
    SETUP_SQL = ("setup_sql", False)
    TEARDOWN = ("teardown", False)
    TEARDOWN_SQL = ("teardown_sql", False)
    SLEEP = ("sleep", False)


class ResponseData(BaseModel):
    """
    其中有一些变量是未被使用的
    """
    url: Text
    is_run: Union[None, bool, Text]
    detail: Text
    response_data: Text
    request_body: Any
    method: Text
    sql_data: Dict
    yaml_data: "TestCase"
    headers: Dict
    cookie: Dict
    assert_data: Dict
    res_time: Union[int, float]
    status_code: int
    teardown: Union[List["TearDown"], None] = None
    teardown_sql: Union[None, List]
    body: Any


class environment(BaseModel):
    name: Text
    password: Text
    host: Text


class browser(Enum):
    CHROMIUM = "chromium"
    FIREFOX = "firefox"
    WEBKIT = "webkit"


class Common(BaseModel):
    project_name: Text
    report_name: Text
    env: "environment"


class run_config(BaseModel):
    browser: Text = browser.CHROMIUM.value
    mode: Text = "headless"
    rerun: int = 0
    max_fail: int = 10
    rerun_delay: int = 2
    window_size: Dict = {
        'height': 1920,
        'width': 1080
    }


class Config(BaseModel):
    common: "Common"
    run_config: "run_config"
    notification_type: Text = '0'
    ding_talk: "DingTalk"
    email: "Email"
    mysql_db: "MySqlDB"
    lark: "Webhook"
    wechat: "Webhook"


@unique
class DependentType(Enum):
    """
    数据依赖相关枚举
    """
    RESPONSE = 'response'
    REQUEST = 'request'
    SQL_DATA = 'sqlData'
    CACHE = "cache"


@dataclass
class TestMetrics:
    """ 用例执行数据 """
    passed: int
    failed: int
    broken: int
    skipped: int
    total: int
    pass_rate: float
    time: Text


if __name__ == '__main__':
    pass

