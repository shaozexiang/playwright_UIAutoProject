# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : conftest.py
"""
import ast
import json
import os
import subprocess
import time

import jsonpath
import pytest
import requests
from playwright.sync_api import Page, BrowserContext, Playwright
from filelock import FileLock
from utils import ensure_path_sep
from utils.cache_process.cache_control import CacheHandler
from utils.other_tools.exceptions import JsonpathExtractionFailed
from utils.other_tools.get_file_path import get_userHome_dir
from utils.process_tools.process_handler import is_port_in_use


def login_status(playwright):
    _browser = playwright.chromium.launch()
    _context = _browser.new_context()
    _page = _context.new_page()
    _page.goto("http://10.0.20.22:17110/#/")
    _page.get_by_placeholder("请输入账号").fill('szx')
    _page.get_by_placeholder("请输入密码").fill('zhifei@123')
    _page.locator("label span").nth(1).check()
    _page.get_by_role("img").nth(3).click()
    _page.wait_for_load_state('networkidle')
    session_data = _page.evaluate('JSON.stringify(sessionStorage)')
    while ast.literal_eval(session_data).get('token') is None:
        session_data = _page.evaluate('JSON.stringify(sessionStorage)')
    _context.close()
    _browser.close()
    return session_data


@pytest.fixture(scope="session", autouse=False)
def store_session_data(playwright: Playwright, worker_id, tmp_path_factory):
    """
    存储session信息
    :return:
    """
    if worker_id == "master":
        session_data = login_status(playwright)
        login_token = ast.literal_eval(session_data).get('token')
        CacheHandler.update_cache(cache_key='login_token', cache_value=login_token)
        CacheHandler.update_cache(cache_key='login_state', cache_value=session_data)
        return

    root_tmp_dir = tmp_path_factory.getbasetemp().parent
    fn = root_tmp_dir / "data.json"
    with FileLock(str(fn) + ".lock"):
        if fn.is_file():
            session_data = json.loads(fn.read_text())
        else:
            session_data = login_status(playwright)
            fn.write_text(json.dumps(str(session_data)))
        login_token = ast.literal_eval(session_data).get('token')
        CacheHandler.update_cache(cache_key='login_token', cache_value=login_token)
        CacheHandler.update_cache(cache_key='login_state', cache_value=session_data)


@pytest.fixture(scope="function", autouse=False)  # 集成测试代码使用该fixture
def keep_login(page: Page, store_session_data, set_allPage_default_time):
    session_storage = CacheHandler.get_cache('login_state')
    session_data = ast.literal_eval(session_storage)
    page.goto("http://10.0.20.22:17110/#/index")
    # 等待页面加载完毕
    try:
        page.evaluate(
            '''
                (session_data) => {
                    for(const [key, value] of Object.entries(session_data)){
                        sessionStorage.setItem(key, value)
                    }
                }
            '''
            , session_data)
    except Exception:
        print("evaluate exception........")
    page.goto("http://10.0.20.22:17110/#/index")


# @todo 还没想好怎么写，暂时先放在这
@pytest.fixture(scope="session", autouse=False)
def connect_exists_browser(playwright):
    """
    检测是否已连接上浏览器
    未连接---》连接上当前的页面
    已链接---》不处理当前的页面
    :return:
    """
    try:
        command = (
                get_userHome_dir() + r'\AppData\Local\ms-playwright\chromium-1140\chrome-win\chrome.exe ' + '--remote-debugging-port=9222' + f'--user-data-dir="{get_userHome_dir()}\PlaywrightDataDir"'
        )
        if is_port_in_use(9222) is False:
            subprocess.Popen(command)
    except Exception:
        pass
    _browser = playwright.chromium.connect_over_cdp(endpoint_url="http://localhost:9222", timeout=5000)
    default_context = _browser.contexts[0]
    default_context.set_default_timeout(5000)
    page = default_context.pages[0]
    page.add_init_script(
        ensure_path_sep("\\js_file\\full_screen.js")
    )
    return page


@pytest.fixture
def set_allPage_default_time(context: BrowserContext):
    """
    设置全部页面的全局最大等待时间
    :param context:
    :return:
    """
    context.set_default_timeout(5000)


@pytest.fixture(scope='session', autouse=False)
def manager_role_login():
    """
    使用管理员的身份登录，用于接口的前置数据
    """
    print("管理员身份获取token登录.......")
    url = "http://10.0.20.22:17110/api/auth/v1/login"
    data = {
        "device": "",
        "password": "FM8SFsu+rLdVV4cRedks3olNv1VTcltH8u5//HeyzIoGDZIjqM3ZXaeP35ZkX4eMxNEGu1LcWsJWfzkwyQGsMZw4llrMLrzMF2cZak0lgzrWlBD6PemdhGgdalaTUc3XNN9H8h/ujUvzZdMf/+iRp5jHWCQ0gmAgu1NfBo3/dd8=",
        "userName": "szx"
    }
    headers = {'Content-Type': 'application/json;charset=UTF-8'}
    res = requests.post(url=url, json=data, headers=headers)
    resp_data = res.json()
    jsonpath_data = jsonpath.jsonpath(resp_data, '$.data.token')
    if jsonpath_data is not False:
        CacheHandler.update_cache(cache_key='login_token', cache_value=jsonpath_data[0])
        print(f"token值为{jsonpath_data[0]}")
    else:
        raise JsonpathExtractionFailed("jsonpath提取失败，无法获取token进行登录，请检查提取数据是否正确")


@pytest.fixture(scope='class', autouse=True)
def clear_class_cache():
    """ 在一个类的测试用例数据执行结束之后清除掉类内的缓存数据"""
    yield
    CacheHandler.clear_clsCache()


@pytest.fixture(scope='function', autouse=True)
def clear_function_cache():
    """ 在单个测试用例执行结束之后清除掉单个测试用例的缓存数据"""
    yield
    CacheHandler.clear_funcCache()

