# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : locator_decorator.py
"""
from utils.logging_tools.log_control import ERROR
from playwright.sync_api import TimeoutError as timeoutExcept


def clean_locator(func):
    def wrapper(self, *args, **kwargs):
        # 执行方法
        result = func(self, *args, **kwargs)

        # 清理逻辑
        locator_list = ['get_by_alt_text', 'get_by_label', 'get_by_placeholder', 'get_by_role', 'get_by_test_id',
                        'get_by_text', 'get_by_title', 'locator', 'first_element_locator', 'nth_element_locator',
                        'last_element_locator', 'filter']
        if str(func.__name__).startswith('__'):
            pass
        elif func.__name__ not in locator_list:  # 特殊处理自定义的私有方法避免访问到__init_instance()or__instance_not_create_error()
            # 这两个方法分别是类内用来实例化locator对象和处理异常
            # pass
            exec(f"self._{self.__class__.__name__}__locator_instance = None")
        return result

    return wrapper


def auto_clean_locatorInstance(cls):
    for attr_name in dir(cls):
        attr = getattr(cls, attr_name)
        # 检查是否是实例方法
        if callable(attr) and not attr_name.startswith('__'):
            # 使用装饰器包装方法
            wrapped = clean_locator(attr)
            setattr(cls, attr_name, wrapped)
    return cls


'''
也可以通过基类的方式去实现相同的效果
'''


# class BasePageMetaClass(type):
#     def __new__(cls, name, base, attrs):
#         for attr_name, attr_value in attrs.items():
#             if callable(attr_value):
#                 attrs[attr_name] = clean_locator(attr_value)
#         return super().__new__(cls, name, base, attrs)
#
# class BasePage(metaclass=BasePageMetaClass)
# 在类的上面增加metaclass=BasePageMetaClass这个代码即可，实际与使用类装饰器并没有差异

def locator_error_log(msg):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                if isinstance(e, timeoutExcept):
                    ERROR.raise_errorException(f"{msg}操作出错，定位超时\n"
                                               f"错误信息为:{e}")
                else:
                    ERROR.raise_errorException("其他异常报错\n"
                                               f"错误信息为:{e}")

        return wrapper

    return decorator


