# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : time_control.py
"""
import inspect
import time
import types
import typing
from datetime import datetime, timedelta
from typing import Text

from playwright.sync_api import Page

from utils.logging_tools.log_control import ERROR


def count_milliseconds():
    """
    计算时间
    :return:
    """
    access_start = datetime.now()
    access_end = datetime.now()
    access_delta = (access_end - access_start) * 1000
    return access_delta


def timestamp_conversion(time_data: Text) -> int:
    """
    时间戳转换，将日期格式转换为时间戳
    :param time_data: 时间
    :return:
    """
    try:
        # 将字符串转化为时间元组 time.struct_time(tm_year=2000, tm_mon=11, tm_mday=30, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=3, tm_yday=335, tm_isdst=-1)
        datetime_format = datetime.strptime(str(time_data), "%Y-%m-%d %H-%M:%S")
        # timestamp = int(
        #     time.mktime(datetime_format.timetuple()) *1000.0
        #     + datetime_format.microsecond /1000.0
        # )
        # 下面为等价语句
        stamp_data = int(datetime.timestamp(datetime_format))
        return stamp_data
    except ValueError as exc:
        raise ValueError('日期格式错误， 需要传入的格式为 %Y-%m-%d %H-%M:%S ') from exc


def time_conversion(time_num: int):
    """
    时间戳转换成日期
    :param time_num:
    :return:
    """
    date_obj = datetime.fromtimestamp(time_num)
    date_string = date_obj.strftime("%Y-%m-%d %H-%M:%S ")
    return date_string


def now_time():
    """
    获取当前的具体时间
    格式为%Y-%m-%d %H-%M:%S
    :return:
    """
    time_format = "%Y-%m-%d %H-%M-%S"
    local_time = time.strftime(time_format, time.localtime())
    return local_time


def now_day():
    """
    获取当前的具体时间
    格式为%Y-%m-%d
    :return:
    """
    time_format = "%Y-%m-%d"
    local_time = time.strftime(time_format, time.localtime())
    return local_time


def execution_duration(times: int):
    """

    :param times: 预计函数执行时间
    :return:
    """

    def decorator(func):
        def swapper(*args, **kwargs):
            res = func(args, kwargs)
            run_time = res.res_time
            if run_time < times:
                ERROR.logger.error(
                    "\n==============================================\n"
                    "测试用例执行时间较长，请关注.\n"
                    "函数运行时间: %s ms\n"
                    "测试用例相关数据: %s\n"
                    "================================================="
                    , run_time, res)
            return res

        return swapper

    return decorator


def scheduled_task(work, time_type='seconds', delay_time=10):
    """
    执行定时任务。但是会卡住整个主线程的执行
    :param work:
    :param time_type:
    :param delay_time:
    :return:
    """
    _now_time = datetime.now()
    time_params = {time_type: delay_time}
    end_time = _now_time + timedelta(**time_params)
    sleep_num = 1  # 睡眠次数
    while end_time > _now_time:
        if sleep_num == 1:
            time.sleep(0.5)
        else:
            time.sleep(sleep_num)
        # 替换掉这个work函数为具体需要执行定时任务的函数
        work()
        sleep_num += 1
        _now_time = datetime.now()


def circular_wait_event(event, page: Page, time_type: str = 'seconds', delay_time=10):
    """
    用于解决定位过程中出现的数据加载问题
    :param work: 执行的函数
    :param page: 传递的page对象，用于执行wait_for_timeout
    :param time_type: 时间的类型[days, seconds,minutes, hours, weeks, milliseconds, microseconds]
    :param delay_time: 持续多长时间
    :return:
    """
    _now_time = datetime.now()
    time_params = {time_type: delay_time}
    end_time = _now_time + timedelta(**time_params)
    sleep_num = 1  # 睡眠次数
    while end_time > _now_time and event is not True:
        if sleep_num == 1:
            page.wait_for_timeout(1 * 200)
        else:
            page.wait_for_timeout(sleep_num * 200)
        sleep_num += 1
        _now_time = datetime.now()


def get_properties(cls):
    """
    获取类的扩展模块的方法的名称，与property注解的作用一致
    :param cls:
    :return:
    """
    properties = []
    for name, obj in inspect.getmembers(cls):
        if isinstance(obj, types.MemberDescriptorType):
            properties.append(name)
    return properties


def get_NowTime_FileName():
    return time.strftime("%Y%m%d%H%M%S", time.localtime())


def get_today_day():
    return datetime.today().day


if __name__ == '__main__':
    result = get_today_day()
    print(result)

