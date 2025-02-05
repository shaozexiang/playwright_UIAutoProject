# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : log_control.py
"""
"""
日志封装，可设置不同等级的日志颜色
日志封装的关键在于如何分发不同的日志等級，通过什么方式去分发不同的请求
日志通过装饰器的方式去分发请求，在装饰器中会分发info和失败的请求
"""
import logging
from logging import handlers
from typing import Text
import colorlog
import time
from utils.other_tools.get_file_path import ensure_path_sep


class LogHandler:
    """ 日志打印封装"""
    # 日志级别关系映射
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    def __init__(
            self,
            filename: Text,
            level: Text = "info",
            when: Text = "D",
            fmt: Text = "%(levelname)-8s%(asctime)s%(name)s:%(filename)s:%(lineno)d %(message)s"
    ):
        self.logger = logging.getLogger(filename)
        if not self.logger.handlers:  # 避免重复注册logger
            formatter = self.log_color()

            # 设置日志格式
            format_str = logging.Formatter(fmt)
            # 设置日志级别
            self.logger.setLevel(self.level_relations.get(level))
            # 创建一个控制台处理器
            screen_output = logging.StreamHandler()
            # 设置屏幕上显示的格式
            screen_output.setFormatter(formatter)
            # 往文件里写入指定间隔时间自动生成文件的处理器
            time_rotating = handlers.TimedRotatingFileHandler(
                filename=filename,
                when=when,
                backupCount=3,
                encoding='utf-8'
            )
            # 设置文件里写入的格式
            time_rotating.setFormatter(format_str)
            # 把对象加到logger里
            if screen_output not in self.logger.handlers:
                self.logger.addHandler(screen_output)
            if time_rotating not in self.logger.handlers:
                self.logger.addHandler(time_rotating)
            self.log_path = ensure_path_sep('\\logs\\log.log')

    @classmethod
    def log_color(cls):
        """ 设置日志颜色 """
        log_colors_config = {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
        }

        formatter = colorlog.ColoredFormatter(
            '%(log_color)s[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s',
            log_colors=log_colors_config
        )
        return formatter

    def raise_errorException(self, message):
        self.logger.error(message)
        raise Exception(message)


now_time_day = time.strftime("%Y-%m-%d", time.localtime())
INFO = LogHandler(ensure_path_sep(f"\\logs\\info-{now_time_day}.log"), level='info')
ERROR = LogHandler(ensure_path_sep(f"\\logs\\error-{now_time_day}.log"), level='error')
WARNING = LogHandler(ensure_path_sep(f'\\logs\\warning-{now_time_day}.log'))

if __name__ == '__main__':
    ERROR.logger.error("测试数据测试测试")
    ERROR.logger.error("测试数据测试测试111111")
    INFO.logger.info("输出Info语句")
    ERROR.raise_errorException("异常报错")
    INFO.logger.info("输出Info语句")



