# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : allure_step_handler.py
@Time : 2025/2/5 23:15
"""
import json
import os.path

import allure
from typing import Text
from utils.other_tools.models import AllureAttachmentType

"""
这里是用于处理allure步骤的方法
分为两种处理方式，第一种处理方式是
"""


def allure_title(title: str) -> None:
    """ allure报告中动态生成用例标题"""
    allure.dynamic.story(title)


def allure_step(step_name: str, content: str):
    """
    为allure报告输出具体步骤
    allure.attach(body, name, attachment_type, extension)
    :param step_name: 附件名称
    :param content: 附件内容
    :return:
    """
    allure.attach(
        body=json.dumps(
            str(content),
            ensure_ascii=False,
            indent=4
        ),
        name=step_name,
        attachment_type=allure.attachment_type.JSON
    )


def allure_attach(source: str):
    """
    allure报告上传附件、图片等其他非文本内容
    除了路径是必填的其他内容均可以为空
    :param source: 文件路径
    :return:
    """
    name = os.path.basename(source)
    file_suffix = source.split('.')[-1]
    _attachment_type = getattr(AllureAttachmentType, file_suffix.upper(), None)
    allure.attach.file(
        source=source,
        name=name,
        attachment_type=_attachment_type if _attachment_type is None else _attachment_type.value,
        extension=None if _attachment_type is None else file_suffix
    )


def allure_step_no(title):
    """
    只需要输出allure的步骤，不需要携带其他信息的情况
    :return:
    """
    try:
        allure.step(title)
    except Exception as ex:
        print(ex)

if __name__ == '__main__':
    pass

