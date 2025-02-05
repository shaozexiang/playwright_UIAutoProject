# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : time_control.py
"""
import time


class TimeHandler:
    @staticmethod
    def get_now_time():
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    @staticmethod
    def get_NowTime_FileName():
        return time.strftime("%Y%m%d%H%M%S", time.localtime())


if __name__ == '__main__':
    result = TimeHandler.get_NowTime_FileName()
    result = TimeHandler.get_now_time()
    print(result)

