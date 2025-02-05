# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : regular_control.py
"""
"""
Desc : 自定义函数调用
"""
import re
import datetime
import random
from datetime import date, timedelta, datetime
from jsonpath import jsonpath
from faker import Faker

from utils.logging_tools.log_control import ERROR


class Context:
    """ 正则替换 """

    def __init__(self):
        self.faker = Faker(locale='zh_CN')

    @classmethod
    def random_int(cls) -> int:
        """
        :return: 随机数
        """
        _data = random.randint(0, 5000)
        return _data

    def get_phone(self) -> int:
        """
        :return: 随机生成手机号码
        """
        phone = self.faker.phone_number()
        return phone

    def get_id_number(self) -> int:
        """

        :return: 随机生成身份证号码
        """

        id_number = self.faker.ssn()
        return id_number

    def get_female_name(self) -> str:
        """

        :return: 女生姓名
        """
        female_name = self.faker.name_female()
        return female_name

    def get_male_name(self) -> str:
        """

        :return: 男生姓名
        """
        male_name = self.faker.name_male()
        return male_name

    def get_email(self) -> str:
        """

        :return: 生成邮箱
        """
        email = self.faker.email()
        return email

    @classmethod
    def get_time(cls) -> str:
        """
        计算当前时间
        :return:
        """
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return now_time

    @classmethod
    def today_date(cls):
        """获取今日时间, 如果需要获取的时间为零点整则去掉注释即可"""
        _today = date.today().strftime("%Y-%m-%d") + " 00:00:00"
        return str(_today)

    @classmethod
    def tomor_date(cls):
        """ 获取明天时间"""
        _tomor_day = (date.today() + +timedelta(days=1)).strftime("%Y-%m-%d") + " 00:00:00"
        return str(_tomor_day)

    @classmethod
    def time_after_week(cls):
        """获取一周后12点整的时间"""

        _time_after_week = (date.today() + timedelta(days=+6)).strftime("%Y-%m-%d") + " 00:00:00"
        return _time_after_week

    @classmethod
    def host(cls) -> str:
        from utils import config
        """ 获取接口域名 """
        return config.common.env.host

    @classmethod
    def app_host(cls) -> str:
        from utils import config
        """获取app的host"""
        return config.app_host

    @classmethod
    def get_file_name(cls, file_path: str):
        """ 获取文件"""
        file_path = cache_regular(file_path)
        return file_path.split('.')[0]


def sql_json(js_path, res):
    """ 提取 sql中的 json 数据 """
    _json_data = jsonpath(res, js_path)[0]
    if _json_data is False:
        raise ValueError(f"sql中的jsonpath获取失败 {res}, {js_path}")
    return _json_data


def sql_regular(value, res=None):
    """
    这里处理sql中的依赖数据，通过获取接口响应的jsonpath的值进行替换
    处理 $json(此为具体的参数)的情况
    :param res: jsonpath使用的返回结果
    :param value:
    :return:
    """
    sql_json_list = re.findall(r"\$json\((.*?)\)\$", value)

    for i in sql_json_list:
        pattern = re.compile(r'\$json\(' + i.replace('$', "\$").replace('[', '\[') + r'\)\$')
        key = str(sql_json(i, res))
        value = re.sub(pattern, key, value, count=1)

    return value


def cache_regular(value):
    from utils.cache_process.cache_control import CacheHandler

    """
    通过正则的方式，读取缓存中的内容
    例：$cache{login_init}
    :param value:
    :return:
    """
    # 正则获取 $cache{login_init}中的值 --> login_init
    # regular_dates = re.findall("\$cache\{(.*?)}", value)
    regular_dates = re.findall("\\$cache{(.*?)}", value)
    # 拿到的是一个list，循环数据
    for regular_data in regular_dates:
        value_types = ['int:', 'bool:', 'list:', 'dict:', 'tuple:', 'float:']
        if any(i in regular_data for i in value_types) is True:  # 处理数据非str类型，需要显示为
            value_types = regular_data.split(":")[0]
            regular_data = regular_data.split(":")[1]
            pattern = re.compile(r'\'\$cache\{' + value_types.split(":")[0] + ":" + regular_data + r'}\'')
        elif any(i in regular_data for i in ['func:', 'cls:']) is True:
            # 处理缓存数据的作用域是类或者函数级别的情况
            value_types = regular_data.split(":")[0]
            regular_data = regular_data.split(":")[1]
            pattern = re.compile(r'\$cache\{' + value_types.split(":")[0] + ":" + regular_data + r"}")
            if 'func' == value_types:
                cache_data = CacheHandler.get_funcCache(regular_data)
            else:
                cache_data = CacheHandler.get_clsCache(regular_data)
            value = re.sub(pattern, str(cache_data), value)
            return value
        else:
            pattern = re.compile(
                '\\$cache\\{' + regular_data.replace('$', "\$").replace('[', '\[') + r'}'
            )
        try:
            cache_data = CacheHandler.get_cache(regular_data)
            # 使用sub方法，替换已经拿到的内容
            value = re.sub(pattern, str(cache_data), value)
        except Exception:
            pass
    return value


def regular(target):
    """
    使用正则替换请求数据
    :return:
    """
    try:
        regular_pattern = r'\${{(.*?)}}'
        while re.findall(regular_pattern, target):
            key = re.search(regular_pattern, target).group(1)
            value_types = ['int:', 'bool:', 'list:', 'dict:', 'tuple:', 'float:']
            if any(i in key for i in value_types) is True:
                func_name = key.split(":")[1].split("(")[0]
                value_name = key.split(":")[1].split("(")[1][:-1]
                if value_name == "":
                    value_data = getattr(Context(), func_name)()
                else:
                    value_data = getattr(Context(), func_name)(*value_name.split(","))
                regular_int_pattern = r'\'\${{(.*?)}}\''
                target = re.sub(regular_int_pattern, str(value_data), target, 1)
            else:
                func_name = key.split("(")[0]
                value_name = key.split("(")[1][:-1]
                if value_name == "":
                    value_data = getattr(Context(), func_name)()
                else:
                    value_data = getattr(Context(), func_name)(*value_name.split(","))
                target = re.sub(regular_pattern, str(value_data), target, 1)
        return target

    except AttributeError:
        ERROR.logger.error("未找到对应的替换的数据, 请检查数据是否正确 %s", target)
        raise
    except IndexError:
        ERROR.logger.error("yaml中的 ${{}} 函数方法不正确，正确语法实例：${{get_time()}}")
        raise


def locator_regular(text):
    """
    格式化定位元素并且输出定位元素的内容
    """
    text = str(text)
    pattern = "selector='(.*?)'"
    # text = '''ERROR   2024-09-06 10:06:06,592D:\person\code\playwright_WEB_uiautomation\logs\error-2024-09-06.log:base_page.py:251 点击操作出错，定位元素为:<Locator frame=<Frame name= url='http://10.0.20.22:17110/#/RouteManagement'> selector='div >> internal:attr=[placeholder="航线类型"i]'>'''
    # text = '''<Locator frame=<Frame name= url='http://10.0.20.22:15090/#/index'> selector='div >> internal:has-text=/^更多$/ >> span >> nth=1'>'''
    re_group = re.search(pattern, text).group(1) if re.search(pattern, text) is not None else None
    if re_group is None:
        return text
    selector_list = re_group.split('>>')
    locator_text = "定位元素为: "
    for i in selector_list:
        if i == selector_list[0]:
            locator_text = locator_text + "首层元素->" + i
        elif 'internal' in i:
            internal_text = i.split(':')[1]
            if "\\u" in internal_text:
                internal_text = internal_text.encode('utf-8').decode('unicode_escape')
                locator_text += "下一层定位元素->" + internal_text[:-1]
            else:
                locator_text += "下一层定位元素->" + internal_text
        elif i == selector_list[len(selector_list) - 1]:
            locator_text += i
        else:
            locator_text += i + "下一层定位元素->"
    return locator_text


if __name__ == '__main__':
    from utils.cache_process.cache_control import CacheHandler
    CacheHandler.set_funcCache('test2', 'test2')
    CacheHandler.set_clsCache('test2', 'test2')
    CacheHandler.set_clsCache('test1', 'test1AAAA')
    text = "$cache{cls:test1}"
    result = cache_regular(text)
    print(result)

