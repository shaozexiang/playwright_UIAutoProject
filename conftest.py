# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : conftest.py
"""
import time

import pytest
from playwright.sync_api import Playwright

# from utils.log_tools.log_control import INFO, ERROR, WARNING
from utils.logging_tools.log_control import INFO,ERROR,WARNING
# 本地插件注册
pytest_plugins = ('plugins.pytest_playwright',)
"""
添加本地插件后需要在 pytest.ini 中禁用 pip 安装的 pytest-playwright 插件
[pytest]
addopts = -p no:playwright
"""


# @todo 还没想好怎么写，暂时先放在这
@pytest.fixture(scope="session", autouse=False)
def check_connection(browser) -> bool:
    """
    检测是否已连接上浏览器
    未连接---》连接上当前的页面
    已链接---》不处理当前的页面
    :return:
    """
    if browser.is_connected() is False:
        pass
    return browser.is_connected()


@pytest.fixture(scope="session")
def browser_size(playwright: Playwright):
    """
    手动获取获取浏览器的分辨率参数
    :return:
    """
    _browser = playwright.chromium.launch(headless=False)
    _context = _browser.new_context()
    _page = _context.new_page()
    _page.goto("http://10.0.20.22:15090/#/")
    browser_size = _page.evaluate(
        '''
        () => {
                return {
                    width: window.innerWidth,
                    height: window.innerHeight
                };
            }
        '''
    )
    yield browser_size


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {
            'width': 1920,
            'height': 1080
        },
        "record_video_size": {
            "width": 1920,
            "height": 1080
        }
        # 服务器上默认不使用有头模式
        # "no_viewport": True,
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        # "args": ["--start-maximized", "--use-gl=angle"],
        "args": ['--use-gl=angle', "--disable-cache"],
        "devtools": False,
    }


def pytest_collection_modifyitems(items):
    """
    测试用例收集完成之后，按照期望的顺序执行测试用例, 这里可以按照用例的节点顺序或者id顺序进行排序
    item.name
    item.nodeid
    :param items: 默认收集的用例顺序
    :return:
    """
    # 期望顺序
    expect_sequence = []
    # 具体执行顺序
    run_items = []
    for i in expect_sequence:
        for item in items:
            if i.name == item.name:
                run_items.append(item)
    for i in run_items:
        run_index = run_items.index(i)
        items_index = items.index(i)
        if run_index != items_index:
            items[run_index], items[items_index] = items[items_index], items[run_items]


def pytest_terminal_summary(terminalreporter):
    """
    收集测试结果，收集不同的结果
    """
    _PASSED = len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
    _ERROR = len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
    _FAILED = len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
    _SKIPPED = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
    _TOTAL = terminalreporter._numcollected
    _TIMES = time.time() - terminalreporter._sessionstarttime
    INFO.logger.error(f"用例总数: {_TOTAL}")
    INFO.logger.error(f"异常用例数: {_ERROR}")
    ERROR.logger.error(f"失败用例数: {_FAILED}")
    WARNING.logger.warning(f"跳过用例数: {_SKIPPED}")
    INFO.logger.info("用例执行时长: %.2f" % _TIMES + " s")
    try:
        _RATE = _PASSED / _TOTAL * 100
        INFO.logger.info("用例成功率: %.2f" % _RATE + " %")
    except ZeroDivisionError:
        INFO.logger.info("用例成功率: 0.00 %")


# @pytest.hookimpl(hookwrapper=False, tryfirst=False)
# def pytest_runtest_makereport(item, call):  # 对于给定的测试用例(item)和调用步骤(call)，返回一个测试报告对象(_pytest.runner.TestReport)
#     """
# 　　每个测试用例执行后，制作测试报告
# 　　:param item:测试用例对象
# 　　:param call:测试用例的测试步骤
# 　　         执行完常规钩子函数返回的report报告有个属性叫report.when
#             先执行when=’setup’ 返回setup 的执行结果
#             然后执行when=’call’ 返回call 的执行结果
#             最后执行when=’teardown’返回teardown 的执行结果
# 　　:return:
# 　　"""
#     # 获取常规钩子方法的调用结果,返回一个result对象
#     out = yield
#     # # 获取调用结果的测试报告，返回一个report对象, report对象的属性包括when（steup, call, teardown三个值）、nodeid(测试用例的名字)、outcome(用例的执行结果，passed,failed)
#     report = out.get_result()
#     # 过滤掉其他的请求信息，只需要将失败的请求信息提交
#     if report.when == 'call':
#         print(out)
#         print(report)
#         print(report.when)
#         # 执行用例的名称
#         print(report.nodeid)
#         # 执行结果
#         print(report.outcome)

