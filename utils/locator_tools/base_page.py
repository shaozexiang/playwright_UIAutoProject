# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : base_page.py
"""
import os.path
import time
import typing
from datetime import datetime, timedelta
from re import Pattern
from typing import Union, Text, Any, List, Optional, Literal

import numpy as np
from playwright.sync_api import TimeoutError as timeoutExcept, Request, Page
from paddleocr import PaddleOCR

from utils.allure_tools.allure_step_handler import allure_attach, allure_step_no
from utils.locator_tools.locator_decorator import locator_error_log
from utils.other_tools.exceptions import FileNotFound
from utils.logging_tools.log_control import ERROR
import allure
from playwright.sync_api import expect, Locator, FrameLocator
from utils.other_tools.get_file_path import ensure_path_sep, get_all_path

from skimage.metrics import structural_similarity as compare_ssim
import cv2

from utils.read_files_tools.regular_control import regular
from utils.time_tools.time_control import get_NowTime_FileName, now_time


class BasePage:
    def __init__(self, page: Page):
        self.__page = page

    def __repr__(self):
        return f"BasePage({self.__page})"

    def create_locatorInstance(self, locator_instance):
        """ 创建实例对象 """
        return CustomLocator(self, locator_instance)

    @allure.step("____定位元素:by_placeholder - 定位文本：{locator_text}")
    def get_by_placeholder(self, locator_text: Text, exact_switch=False) -> "CustomLocator":
        """
        通过<input  placeholder=""> placeholder属性值获取定位元素对象
        """
        locator_instance = self.__page.get_by_placeholder(locator_text, exact=exact_switch)
        return self.create_locatorInstance(locator_instance)

    @allure.step("____定位元素:by_text - 定位文本： {locator_text}")
    def get_by_text(self, locator_text: Text, exact=False) -> "CustomLocator":
        """
        通过<span text=""> 文本值获取定位元素对象
        :param locator_text: 定位元素
        :param exact: 是否区分大小写和全字符串
        :return:
        """
        locator_instance = self.__page.get_by_text(locator_text, exact=exact)
        return self.create_locatorInstance(locator_instance)

    @allure.step("____定位元素:by_alt_text - 定位文本： {locator_text}")
    def get_by_alt_text(self, locator_text: Text, exact_switch=False) -> "CustomLocator":
        """
        通过<img alt=""> 图片悬停属性值获取定位元素对象
        :param locator_text: 定位元素
        :param exact_switch: 是否区分大小写和全字符串
        :return:
        """
        locator_instance = self.__page.get_by_alt_text(locator_text, exact=exact_switch)
        return self.create_locatorInstance(locator_instance)

    @allure.step("____定位元素:by_title - 定位文本： {locator_text}")
    def get_by_title(self, locator_text: Text, exact_switch=False) -> "CustomLocator":
        """
        通过<span title="count">属性值获取定位元素对象
        :param locator_text: 定位元素
        :param exact_switch: 是否区分大小写和全字符串
        :return:
        """
        locator_instance = self.__page.get_by_title(locator_text, exact=exact_switch)
        return self.create_locatorInstance(locator_instance)

    @allure.step("____定位元素:by_testId - 定位文本： {locator_text}")
    def get_by_test_id(self, locator_text: Text) -> "CustomLocator":
        """
        通过设置的test-id标签获取定位元素对象
        :param locator_text:
        :return:
        """
        locator_instance = self.__page.get_by_test_id(locator_text)
        return self.create_locatorInstance(locator_instance)
da
    @allure.step("____定位元素:by_label - 定位文本： {locator_text}")
    def get_by_label(
            self,
            locator_text: Text,
            exact_switch=False,
    ) -> "CustomLocator":
        """
        通过label值获取定位元素对象
        :param locator_text: 定位元素
        :param exact_switch: 是否区分大小写和全字符串
        :return:
        """
        locator_instance = self.__page.get_by_label(locator_text, exact=exact_switch)
        return self.create_locatorInstance(locator_instance)

    @allure.step("____定位元素:_locator - 定位文本： {locator}")
    def locator(self, locator: str, has_text=None, has_not_text=None, has=None,
                has_not=None,
                ) -> "CustomLocator":
        locator_instance = self.__page.locator(
            locator,
            has_text=has_text,
            has_not_text=has_not_text,
            has=has,
            has_not=has_not
        )
        return self.create_locatorInstance(locator_instance)

    @allure.step("____定位元素:by_role - 定位文本： {locator}")
    def get_by_role(self, locator, name=None, exact=None) -> "CustomLocator":
        """
        通过ARIA属性值获取定位元素对象
        :param exact:
        :param name:
        :param locator: 定位元素
        :return:
        """
        locator_instance = self.__page.get_by_role(locator, name=name, exact=exact)
        return CustomLocator(self, locator_instance)

    def click(self, locator: str, **kwargs) -> None:
        if locator is not None:
            self.locator(locator).click(**kwargs)

    def pause(self):
        self.__page.pause()

    def wait_for_load(self):
        try:
            self.__page.wait_for_load_state('networkidle')
        except Exception as ex:
            ERROR.logger.error(f"报错信息为：{ex}")

    def wait_for_request_finished(self):
        def request_handler(request: Request):
            response = request.response()
            status = response.status
            if status != 200:
                raise Exception("等待请求失败.....")

        self.__page.on("requestfinished", request_handler)

    def route_request(self, url):
        host = regular("${{host()}}") + url

        def intercept_request(route):
            print("now_time=" + now_time())
            time.sleep(2)  # 等待2秒
            print("now_time=" + now_time())
            route.continue_()  # 继续请求
            print("now_time=" + now_time())
            # 拦截特定请求

        self.__page.route(host, intercept_request)

    @allure.step("--> 访问页面，路由：{url}，超时时间： {timeout} 秒")
    def visit(self, url, timeout=5):
        """
        访问页面
        :param url:
        :param timeout:
        :return:
        """
        if self.__page.url == url:
            self.refresh()
        else:
            self.__page.goto(url, timeout=timeout * 1000)

    def wait_for_timeout(self, timeout):
        """
        增加
        :param timeout:
        :return:
        """
        self.__page.wait_for_timeout(timeout)

    @allure.step("____刷新页面")
    def refresh(self):
        """
        刷新页面
        :return:
        """
        self.__page.reload()

    def wait_for_upload_finished(self, url):
        """ 等待上传成功"""
        finish_tag = False

        def request_handler(request):
            if url not in request.url:
                global finish_tag
                finish_tag = True
            time.sleep(0.5)

        while finish_tag is False:
            self.__page.on("request", request_handler)

    @allure.step("____鼠标移动")
    def mouse_move(self, x_position, y_position, step=None):
        self.__page.mouse.move(x_position, y_position, steps=step)

    @allure.step("____鼠标下压")
    def mouse_down(self, button=None):
        self.__page.mouse.down(button=button)

    @allure.step("____鼠标松开")
    def mouse_up(self, button=None):
        self.__page.mouse.up(button=button)

    def _screenshot(self, locator: Locator) -> Text:
        """
        截取用于图像处理的照片
        """
        path = None
        try:
            path = ensure_path_sep("\\file\\error_image\\" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.jpeg')
            self.__page.screenshot(path=path, full_page=True, mask=[locator], mask_color='#00000')
            return path
        except timeoutExcept as e:
            ERROR(f"调用page保存图像异常\n"
                  f"路径为{path}\n"
                  f"异常原因为: {e}")

    def highlight_locator_element(self, locator):
        """
        高亮定位元素,并且将元素放入到allure报告中
        :param locator:
        :return:
        """
        path = ensure_path_sep(f"\\file\\image\\screen_image\\{get_NowTime_FileName()}" + ".jpeg")
        try:
            self.__page.screenshot(path=path, type='jpeg', full_page=True)
            box = locator.bounding_box(timeout=2000)
            x, y, width, height = int(box['x']), int(box['y']), int(box['width']), int(box['height'])
            screen_image = cv2.imread(path)
            cv2.rectangle(screen_image, (x, y), (x + width, y + height), (0, 255, 0), 2)
            try:
                cv2.imwrite(path, screen_image)
            except Exception as ex:
                raise Exception(f"cv2 write error....{ex}")
            allure_attach(path)
        except Exception as e:
            allure_step_no("无法获取到元素位置，请检查元素是否可见、存在")
            allure.attach(path)
            # raise LocatorNotVisibleError("找不到定位元素，请检查定位元素是否定位成功")

    @locator_error_log("图像比较")
    def cmp_img(self, vp_name: Text, locator: Locator, threshold: float = 99) -> bool:
        """
        通过图像比较图片之间的差异，用于无法直接定位到元素进行比对，只能通过图像的形式进行比对
        """
        path = self._screenshot(locator)
        vp_path = ensure_path_sep("\\file\\image\\verify_image\\" + vp_name)
        # 需要注意imread存放的并不是真正的照片而是存放了一个数据矩阵，所以当路径不正确的时候只会返回一个
        vp_img = cv2.imread(vp_path, cv2.COLOR_BGR2GRAY)
        target_img = cv2.imread(path, cv2.COLOR_BGR2GRAY)
        height, width, _ = vp_img.shape
        if vp_img is None:
            ERROR(f"读取照片路径失败\n"
                  f"照片路径为: {vp_path}")
            return False
        target_gray = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)
        vp_gray = cv2.cvtColor(vp_img, cv2.COLOR_BGR2GRAY)
        # 前者表示相似度，后者表示数据矩阵
        (diff, s) = compare_ssim(target_gray, vp_gray, full=True)
        if diff > threshold:
            return True
        diff = (diff * 255).astype("utf-8")
        dst = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # 只计算了外部的轮廓
        cnts = cv2.findContours(dst.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if cnts:
            for c in cnts:
                (x, y, w, h) = cv2.boundingRect(c)
                # 绘制图像
                cv2.rectangle(target_img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                path = ensure_path_sep(
                    "\\file\\image\\error_image\\cmp_error" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.jpeg')
        cv2.imwrite(path, target_img)
        allure_attach(path)

    def imagePresent(self, vp_name, locator: Locator, threshold: float) -> bool:
        """
        通过图像识别判断图像是否出现在定位元素的位置
        :param vp_name: 照片名称
        :param locator: 定位元素
        :param threshold: threshold < 1才有效
        :return:
        """
        path1 = self._screenshot(locator)
        path2 = ensure_path_sep(f"\\file\\image\\error_image\\{vp_name}.jpeg")
        original_img = cv2.imread(path1)
        template_img = cv2.imread(path2)
        original_gray = cv2.cvtColor(original_img, cv2.COLOR_RGB2GRAY)
        template_gray = cv2.cvtColor(template_img, cv2.COLOR_RGB2GRAY)
        # 归一化相关系数处理
        result = cv2.matchTemplate(original_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        # 这里获取到的结果是列和行的参数
        loc = np.where(result > threshold)
        template_loc = []
        for pt in zip(*loc[::-1]):
            pt1 = pt
            pt2 = (pt[0] + template_img.shape[1], pt[1] + template_img.shape[0])
            cv2.rectangle(original_img, pt1, pt2, (0, 0, 255), 2)
            # 记录位置信息
            template_loc.append([pt1, pt2])
        path = ensure_path_sep("\\file\\image\\error_image\\test2.jpeg")
        cv2.imwrite(path, original_img)
        if len(template_loc) == 0:
            return False
        return True

    def getOcrText(self, locator: Locator) -> List[str]:
        """
        返回识别到的文本
        :return: 返回None or 照片区域内的文本
        """
        path = self._screenshot(locator)
        paddler = PaddleOCR()
        img = cv2.imread(path)  # 打开需要识别的图片
        result = paddler.ocr(img)[0]
        ocr_text = []
        if result is None:
            raise KeyError(f"ocr识别失败，照片路径为{path}，请检查照片文件为可识别文件")
        for i in result:
            diff = i[-1][1]
            if diff > 0.99:
                ocr_text.append(i[-1][1])
        return ocr_text

    def have_title(self, title: Union[str]) -> None:
        """ 断言：当前页面的标题 """
        expect(self.__page).to_have_title(title)

    @allure.step("____网页不具有标题 - {title}")
    def not_have_title(self, title: Union[str]) -> None:
        """ 断言：当前页面不含有标题 """
        expect(self.__page).not_to_have_title(title)

    @allure.step("____页面路径是 - {url}")
    def have_url(self, url: Union[str]) -> None:
        """ 断言：检查页面是否存在指定的 URL；存在则通过，不存在则失败； """
        expect(self.__page).to_have_url(url)

    @allure.step("____页面路径不是 - {url}")
    def not_have_url(self, url: str) -> None:
        """ 断言：检查页面是否存在指定的 URL；不存在则通过，存在则失败；"""
        expect(self.__page).not_to_have_url(url)

    @allure.step("____下载文件 --> {locator}")
    def wait_for_download(self, locator: typing.Union["CustomLocator", Locator]) -> None:
        """
        等待下载成功, 需要传递的控件为【点击该控件后会执行下载动作】
        :param locator: 元素定位
        """
        locator = locator.get_locatorInstance if isinstance(locator, CustomLocator) else locator
        with self.__page.expect_download(timeout=30 * 1000) as download_info:
            locator.click()
        download = download_info.value
        download_file_path = ensure_path_sep(f"\\file\\ui_export_file\\{download.suggested_filename}")
        download.save_as(download_file_path)
        if not os.path.exists(download_file_path):
            raise FileNotFound(f"文件下载异常，文件路径为{download_file_path}")

    @locator_error_log("执行js脚本")
    @allure.step("____执行js脚本 - {js}")
    def execute_js(self, js, *args) -> None:
        """
        执行JavaScript脚本, 因为evaluate 是执行JavaScript语句所以需要保证语句执行完毕后再往后执行
        :param js:
        :param args:
        :return:
        """
        self.__page.evaluate(js, args)


class CustomLocator:
    """ 只负责所有的定位元素操作"""

    def __init__(self, base_page, locator_instance):
        self.base_page = base_page
        self.__locator_instance: Locator = locator_instance

    def __repr__(self):
        return f"CustomLocator({self.base_page} ------- {self.__locator_instance})"

    @property
    def get_locatorInstance(self):
        return self.__locator_instance

    def wait_for_locator_hidden(self):
        self.__locator_instance.is_visible()
        while self.__locator_instance.is_visible():
            time.sleep(0.5)

    # ------------------------------操作------------------------------------ #

    def iframe_locator(self, locator):
        """ 处理iframe页面的情况"""
        locator_instance = self.__locator_instance.frame_locator(locator)
        return CustomLocator(self.base_page, locator_instance)

    @allure.step("____定位元素:by_role - 定位文本： {locator}")
    def get_by_role(self, locator, name=None, exact=None) -> "CustomLocator":
        """
        通过ARIA属性值获取定位元素对象
        :param exact:
        :param name:
        :param locator: 定位元素
        :return:
        """
        locator_instance = self.__locator_instance.get_by_role(locator, name=name, exact=exact)
        self.__locator_instance.or_()
        return CustomLocator(self.base_page, locator_instance)

    @allure.step("____定位元素:by_placeholder - 定位文本：{locator_text}")
    def get_by_placeholder(self, locator_text: Text, exact_switch=False) -> "CustomLocator":
        """
        通过<input  placeholder=""> placeholder属性值获取定位元素对象
        """
        locator_instance = self.__locator_instance.get_by_placeholder(locator_text, exact=exact_switch)
        return CustomLocator(self.base_page, locator_instance)

    @allure.step("____定位元素:by_text - 定位文本： {locator_text}")
    def get_by_text(self, locator_text: Text, exact=False) -> "CustomLocator":
        """
        通过<span text=""> 文本值获取定位元素对象
        :param locator_text: 定位元素
        :param exact: 是否区分大小写和全字符串
        :return:
        """
        locator_instance = self.__locator_instance.get_by_text(locator_text, exact=exact)
        return CustomLocator(self.base_page, locator_instance)

    @allure.step("____定位元素:by_alt_text - 定位文本： {locator_text}")
    def get_by_alt_text(self, locator_text: Text, exact_switch=False) -> "CustomLocator":
        """
        通过<img alt=""> 图片悬停属性值获取定位元素对象
        :param locator_text: 定位元素
        :param exact_switch: 是否区分大小写和全字符串
        :return:
        """
        locator_instance = self.__locator_instance.get_by_alt_text(locator_text, exact=exact_switch)
        return CustomLocator(self.base_page, locator_instance)

    @allure.step("____定位元素:by_title - 定位文本： {locator_text}")
    def get_by_title(self, locator_text: Text, exact_switch=False) -> "CustomLocator":
        """
        通过<span title="count">属性值获取定位元素对象
        :param locator_text: 定位元素
        :param exact_switch: 是否区分大小写和全字符串
        :return:
        """
        locator_instance = self.__locator_instance.get_by_title(locator_text, exact=exact_switch)
        return CustomLocator(self.base_page, locator_instance)

    @allure.step("____定位元素:by_testId - 定位文本： {locator_text}")
    def get_by_test_id(self, locator_text: Text) -> "CustomLocator":
        """
        通过设置的test-id标签获取定位元素对象
        :param locator_text:
        :return:
        """
        locator_instance = self.__locator_instance.get_by_test_id(locator_text)
        return CustomLocator(self.base_page, locator_instance)

    @allure.step("____定位元素:by_label - 定位文本： {locator_text}")
    def get_by_label(
            self,
            locator_text: Text,
            exact_switch=False,
    ) -> "CustomLocator":
        """
        通过label值获取定位元素对象
        :param locator_text: 定位元素
        :param exact_switch: 是否区分大小写和全字符串
        :return:
        """
        locator_instance = self.__locator_instance.get_by_label(locator_text, exact=exact_switch)
        return CustomLocator(self.base_page, locator_instance)

    @allure.step("____定位元素:_locator - 定位文本： {locator}")
    def locator(self, locator: Union[str, "CustomLocator", Locator], has_text=None, has_not_text=None,
                has: "CustomLocator" = None,
                has_not: "CustomLocator" = None,
                ):
        locator_instance = self.__locator_instance.locator(
            locator.get_locatorInstance if isinstance(locator, CustomLocator) else locator,
            has_text=has_text,
            has_not_text=has_not_text,
            has=has.get_locatorInstance if has is not None else None,
            has_not=has_not.get_locatorInstance if has is not None else None
        )
        return CustomLocator(self.base_page, locator_instance)

    @allure.step("____基于当前定位器过滤 ")
    def filter(self, has_text=None, has_not_text=None, has: "CustomLocator" = None,
               has_not: "CustomLocator" = None) -> "CustomLocator":
        """
        过滤已有的locator对象
        """
        locator_instance = self.__locator_instance.filter(has_text=has_text, has_not_text=has_not_text)
        if has is not None:
            locator_instance = self.__locator_instance.filter(has_text=has_text, has_not_text=has_not_text,
                                                              has=has.get_locatorInstance,
                                                              has_not=has_not)
        elif has_not is not None:
            locator_instance = self.__locator_instance.filter(has_text=has_text, has_not_text=has_not_text, has=has,
                                                              has_not=has_not.get_locatorInstance)

        return CustomLocator(self.base_page, locator_instance)

    @allure.step("____")
    @allure.step("____通过序号定位元素 - 序号:{index}")
    def nth_element_locator(self, index: int):
        locator_instance = self.__locator_instance.nth(index)
        return CustomLocator(self.base_page, locator_instance)

    @allure.step("____获取最后一个匹配的元素")
    @property
    def last_element_locator(self) -> "CustomLocator":
        locator_instance = self.__locator_instance.last
        return CustomLocator(self.base_page, locator_instance)

    @allure.step("____获取第一个匹配的元素")
    @property
    def first_element_locator(self) -> "CustomLocator":
        locator_instance = self.__locator_instance.first
        return CustomLocator(self.base_page, locator_instance)

    def both_locator(self, locator: "CustomLocator"):
        locator_instance = self.__locator_instance.and_(locator.get_locatorInstance)
        return CustomLocator(self.base_page, locator_instance)

    def blur(self):
        """ 让聚焦的元素失去焦点"""
        self.__locator_instance.blur()

    @locator_error_log("点击")
    @allure.step("____点击")
    def click(
            self,
            **kwargs,
    ) -> None:

        self.base_page.highlight_locator_element(self.__locator_instance)
        self.__locator_instance.click(**kwargs)

    @locator_error_log("取消勾选")
    @allure.step("____取消勾选")
    def uncheck(self, **kwargs):
        # 取消勾选
        try:
            self.base_page.highlight_locator_element(self.__locator_instance)
            self.__locator_instance.uncheck(**kwargs)
        except timeoutExcept:
            ERROR.logger.error(f"取消勾选操作出错, 定位对象为{self.__locator_instance}\n")

    @locator_error_log("勾选")
    @allure.step("____勾选 - {locator}")
    def check(self, ) -> None:
        self.base_page.highlight_locator_element(self.__locator_instance)
        self.__locator_instance.check()

    @locator_error_log("双击")
    @allure.step("____双击")
    def dbl_click(self, **kwargs):
        self.base_page.highlight_locator_element(self.__locator_instance)
        self.__locator_instance.dblclick(**kwargs)

    @locator_error_log("悬浮")
    @allure.step("____悬浮")
    def hover(self, locator):
        if locator is not None and isinstance(locator, CustomLocator):
            self.__locator_instance = locator
        self.base_page.highlight_locator_element(self.__locator_instance)
        self.__locator_instance.hover()

    @locator_error_log("输入")
    @allure.step("____输入")
    def fill(self, value, locator=None) -> None:
        if locator is not None and isinstance(locator, CustomLocator):
            self.__locator_instance = locator
        self.base_page.highlight_locator_element(self.__locator_instance)
        self.__locator_instance.fill(str(value))

    def is_visible(self, timeout=None) -> bool:
        return self.__locator_instance.is_visible(timeout=timeout)

    @locator_error_log("模拟键盘键入")
    @allure.step("____键入")
    def type(self, content):
        """
        discourage function
        通过键盘模拟输入内容
        :param content:
        :return:
        """
        self.base_page.highlight_locator_element(self.__locator_instance)
        self.__locator_instance.click()
        self.__locator_instance.type(content)

    @locator_error_log("option标签选择")
    @allure.step("____选择 - {option} ")
    def select_option(self, value):
        """
        option多选框操作
        :param value: value属性值或者文本值
        :return:
        """
        self.base_page.highlight_locator_element(self.__locator_instance)
        self.__locator_instance.select_option(value)

    @locator_error_log("上传文件")
    @allure.step("____上传文件 - {file_name} ")
    def upload_file(self, file_name: Union[str, List], upload_type: Literal["multiple", "dir"] = None) -> None:
        """
        上传文件功能
        :param upload_type:
        :param file_name:
        :return:
        """
        if upload_type is None:
            file_path = ensure_path_sep(f"\\file\\ui_upload_file\\{file_name}")
        else:
            if upload_type == 'multiple':
                file_path = get_all_path(ensure_path_sep(f"\\file\\ui_upload_file\\{file_name}"))
                for i in file_path:
                    if os.path.exists(i) is False:
                        raise ValueError(f"附件未找到，请检查输入路径{i}是否正确")
            elif upload_type == 'dir':
                file_path = ensure_path_sep(f"\\file\\ui_upload_file\\{file_name}")
            else:
                raise KeyError(f"上传文件不支持传入该参数类型，请检查类型值是否正确{upload_type}")
        self.__locator_instance.set_input_files(file_path, timeout=10 * 1000)

    @locator_error_log("执行js脚本")
    @allure.step("____执行js脚本 - {js}")
    def execute_js(self, js, *args) -> None:
        """
        执行JavaScript脚本
        :param js:
        :param args:
        :return:
        """
        self.__locator_instance.evaluate(js, args)

    @locator_error_log("模拟键盘按压操作")
    @allure.step("____按{keyboard}键 --> {locator}")
    def press(self, keyboard: str) -> None:
        self.__locator_instance.press(keyboard)

    @allure.step("____切换到iframe界面中 定位为---> {iframe_locator}")
    def iframe_switch(self, iframe_locator: Text) -> "CustomLocator":
        frame_instance = self.__locator_instance.frame_locator(iframe_locator)
        return CustomLocator(self.base_page, frame_instance)

    # ------------------------------查询------------------------------------ #
    @locator_error_log("获取元素文本值")
    @allure.step("____获取元素文本值")
    def text_content(self):
        return self.__locator_instance.text_content()

    @locator_error_log("获取内部文本值")
    @allure.step("____获取内部文本值 - {}")
    def get_inner_text(self) -> Optional[
        Text]:
        """
        获取内部文本值
        :param locator_method: 请求方法参数
        :param locator:
        :param iframe_locator:
        :return: 内部文本值
        """
        return self.__locator_instance.inner_text()

    @locator_error_log("获取html值")
    @allure.step("____获取html值 - {} ")
    def get_inner_html(self, ):
        """
        获取html值
        :return: html值
        """
        return self.__locator_instance.inner_html()

    @locator_error_log("获取页面的所有文本值")
    @allure.step("____ 获取页面的所有文本值 - 定位为{locator}")
    def get_all_text_contents(self):
        return self.__locator_instance.all_text_contents()

    @locator_error_log("获取元素的属性值")
    @allure.step("____ 获取元素的属性值")
    def get_attribute(self, attr_name) -> Optional[Text]:
        value = self.__locator_instance.get_attribute(attr_name)
        return value

    def element_is_visible(self, timeout=10 * 1000):
        self.__locator_instance.is_visible(timeout=timeout)

    def element_is_disabled(self):
        return self.__locator_instance.is_disabled()

    def highlight_element(self):
        self.__locator_instance.highlight()

    # ------------------------------断言------------------------------------ #

    @allure.step("断言定位元素下有文本 - {text}")
    def have_text(self, text: str) -> None:
        """
        断言：某个元素是否为指定的文本
        """
        expect(self.__locator_instance).to_have_text(text)
        self.base_page.highlight_locator_element(self.__locator_instance)

    @locator_error_log("断言包含文本")
    @allure.step("断言定位元素包含文本 - {text} ")
    def contain_text(self, text) -> None:
        """ 断言：某个元素是否含有指定的文本
        应用场景：当你需要确认某个元素（如段落、标题、通知等）内部是否包含指定的文本时使用。这不仅适用于输入框，也适用于任何可包含文本的元素
        如果断言的是列表需要保证列表的每一个值可找到
        """
        expect(self.__locator_instance).to_contain_text(text)
        self.base_page.highlight_locator_element(self.__locator_instance)

    @locator_error_log("断言表单元素包含值")
    @allure.step("___元素 包含 - {value}")
    def is_element_have_value(self, value: str = None) -> None:
        """ 断言：验证元素是否具有指定的值
         应用场景：当你需要验证表单元素（如输入框、下拉菜单等）的当前值时使用。例如，确认用户输入的内容是否正确
         """
        expect(self.__locator_instance).to_have_value(value)
        self.base_page.highlight_locator_element(self.__locator_instance)

    @locator_error_log("断言元素含有元素值")
    @allure.step("____元素 属性 - {attr_name} 其值是 - {value}")
    def is_element_attr_have_value(self, attr_name: str,
                                   value: str) -> None:
        """
        断言：验证元素的某个属性具有指定的值
        :param locator: 元素定位
        :param attr_name: 元素属性名称
        :param value: 文本内容
        """
        self.base_page.highlight_locator_element(self.__locator_instance)
        assert value == self.get_attribute(attr_name)

    @locator_error_log("断言元素选中")
    @allure.step("____元素 - 被选中")
    def is_element_checked(self) -> None:
        """
        断言：验证复选框是否被选中.
        """
        expect(self.__locator_instance).to_be_checked()
        self.base_page.highlight_locator_element(self.__locator_instance)

    @locator_error_log("断言元素被禁用")
    @allure.step("____元素 - 被禁用")
    def is_element_disabled(self, locator: Union[Locator, None]) -> None:
        """
        断言：验证元素是否被禁用
        """
        self.__locator_instance = locator if isinstance(locator, Locator) else self.__locator_instance

        expect(self.__locator_instance).to_be_disabled()
        self.base_page.highlight_locator_element(self.__locator_instance)

    @locator_error_log("断言元素可编辑")
    @allure.step("____元素 断言 - 可编辑")
    def is_element_editable(self, locator: Union[Locator, None]) -> None:
        """
        断言：验证元素是否可编辑
        :return:
        """
        self.__locator_instance = locator if isinstance(locator, Locator) else self.__locator_instance

        expect(self.__locator_instance).to_be_editable()
        self.base_page.highlight_locator_element(self.__locator_instance)

    @locator_error_log("断言容器为空")
    @allure.step("____元素 断言 - 元素容器为空")
    def is_element_empty(self, locator: Union[Locator, None]) -> None:
        """ 断言：验证容器是否为空 """
        self.__locator_instance = locator if isinstance(locator, Locator) else self.__locator_instance
        expect(self.__locator_instance).to_be_empty()
        self.base_page.highlight_locator_element(self.__locator_instance)

    @locator_error_log("断言元素启用")
    @allure.step("____元素 断言 - 元素启用")
    def is_element_enabled(self, locator: Union[Locator, None]) -> None:
        """ 断言：验证元素是否启用 """
        self.__locator_instance = locator if isinstance(locator, Locator) else self.__locator_instance
        expect(self.__locator_instance).to_be_enabled()
        self.base_page.highlight_locator_element(self.__locator_instance)

    @locator_error_log("断言元素聚焦")
    @allure.step("____元素 断言 - 元素聚焦")
    def is_element_focused(self, locator: Union[Locator, None]) -> None:
        """ 断言：验证元素是否获得焦点 """
        self.__locator_instance = locator if isinstance(locator, Locator) else self.__locator_instance
        expect(self.__locator_instance).to_be_focused()
        self.base_page.highlight_locator_element(self.__locator_instance)

    @locator_error_log("断言元素隐藏")
    @allure.step("____元素 断言 - 元素隐藏")
    def is_element_hidden(self, locator: Union[Locator, None]) -> None:
        """ 断言：验证元素是否隐藏 """
        self.__locator_instance = locator if isinstance(locator, Locator) else self.__locator_instance
        expect(self.__locator_instance).to_be_focused()
        self.base_page.highlight_locator_element(self.__locator_instance)

    @locator_error_log("断言元素可见")
    @allure.step("____元素 断言 - 元素可见")
    def is_element_visible(self, locator: Union[Locator, None] = None) -> None:
        """ 断言：验证元素是否可见 """
        self.__locator_instance = locator if isinstance(locator, Locator) else self.__locator_instance
        expect(self.__locator_instance).to_be_visible()
        self.base_page.highlight_locator_element(self.__locator_instance)

    @locator_error_log("断言元素具有属性")
    @allure.step("____元素 断言 - 元素具有属性 - {attr_name}")
    def is_element_have_attr(self, attr_name: str, locator: Union[Locator, None] = None) -> None:
        """ 断言：验证元素是否具有指定的属性 """
        self.__locator_instance = locator if isinstance(locator, Locator) else self.__locator_instance
        expect(self.__locator_instance).to_have_attribute(attr_name)
        self.base_page.highlight_locator_element(self.__locator_instance)

    @locator_error_log("断言元素元素具有类")
    @allure.step("____元素 断言 - 元素具有类 - {class_name}")
    def is_element_have_class(self, class_name: str, locator: Union[Locator, None] = None) -> None:
        """ 断言：验证元素是否具有指定的属性 """
        self.__locator_instance = locator if isinstance(locator, Locator) else self.__locator_instance
        expect(self.__locator_instance).to_have_class(class_name)
        self.base_page.highlight_locator_element(self.__locator_instance)

    @locator_error_log("断言元素元素个数")
    @allure.step("____元素 断言 - 元素个数 - {elem_count}")
    def is_element_count(self, elem_count: int, locator: Union[Locator, None] = None) -> None:
        """ 断言：验证元素个数是否与期望值相等 """
        self.__locator_instance = locator if isinstance(locator, Locator) else self.__locator_instance
        expect(self.__locator_instance).to_have_count(elem_count)
        self.base_page.highlight_locator_element(self.__locator_instance)

    @locator_error_log("断言元素具有CSS属性")
    @allure.step("____元素 断言 - 元素具有CSS - {class_name}")
    def is_element_have_css(self, css_value: Union[str, Pattern[str]], locator: Union[Locator, None] = None) -> None:
        """
        断言：验证元素个数是否与期望值相等
        :param locator: 元素定位
        :param css_value: css属性，接收str以及正则表达式， 例如"button"， 或者"display", "flex"
        """
        self.__locator_instance = locator if isinstance(locator, Locator) else self.__locator_instance
        expect(self.__locator_instance).to_have_class(css_value)
        self.base_page.highlight_locator_element(self.__locator_instance)

    @locator_error_log("断言元素具有特定id")
    @allure.step("____元素 断言 - 元素具有属性 - {id_name}")
    def is_element_have_id(self, id_name: str, locator: Union[Locator, None] = None) -> None:
        """
        断言：验证元素是否具有指定的ID
        :param locator: 元素定位
        :param id_name: 元素id属性
        """
        self.__locator_instance = locator if isinstance(locator, Locator) else self.__locator_instance
        expect(self.__locator_instance).to_have_css(id_name)
        self.base_page.highlight_locator_element(self.__locator_instance)

    @locator_error_log("断言元素具有属性")
    @allure.step("____元素 断言 - 元素具有特定js属性 - {js_value}")
    def is_element_have_js_property(self, js_value: str, locator: Union[Locator, None] = None) -> None:
        """
        断言：用于验证元素是否具有指定的JavaScript属性
        :param locator: 元素定位
        :param js_value: 元素id属性
        """
        self.__locator_instance = locator if isinstance(locator, Locator) else self.__locator_instance
        expect(self.__locator_instance).to_have_js_property(js_value)
        self.base_page.highlight_locator_element(self.__locator_instance)

    def bounding_box(self):
        box = self.__locator_instance.bounding_box(timeout=2000)
        x, y, width, height = int(box['x']), int(box['y']), int(box['width']), int(box['height'])
        return x, y, width, height

