#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a sample Python script.
import os
import pytest

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Press the green button in the gutter to run the script.
import shutil
from utils import ensure_path_sep, config
from utils.allure_tools.allure_report_data import AllureDataCollect
from utils.logging_tools.log_control import INFO
from utils.notify_tools.ding_talk import DingTalkSendMsg
from utils.notify_tools.lark import FeiShuTalkChatBot
from utils.notify_tools.send_mail import SendEmail
from utils.notify_tools.wechat_send import WeChatSend
from utils.other_tools.models import NotificationType


def run():
    allure_result_path = ensure_path_sep("\\output\\report\\tmp")
    allure_html_path = ensure_path_sep("\\output\\report\\html")
    try:
        # 输出log信息
        INFO.logger.info(
            """
                             _    _         _      _____         _
              __ _ _ __ (_)  / \\  _   _| |_ __|_   _|__  ___| |_
             / _` | '_ \\| | / _ \\| | | | __/ _ \\| |/ _ \\/ __| __|
            | (_| | |_) | |/ ___ \\ |_| | || (_) | |  __/\\__ \\ |_
             \\__,_| .__/|_/_/   \\_\\__,_|\\__\\___/|_|\\___||___/\\__|
                  |_|
                  开始执行{}项目...
                """.format(config.common.project_name)
        )
        arg_list = [
            f"--alluredir={allure_result_path}",
            "--clean-alluredir",
            # f"--rerun-={config.run_config.rerun}",
            # f"--reruns-delay={config.run_config.reruns_delay}"
        ]
        pytest.main(arg_list)
        # 写入报告，这里如果是构建后操作的话就不需要设置手动生成allure报告
        os.system(f'allure generate {allure_result_path} -o {allure_html_path} --clean')
        allure_data = AllureDataCollect.get_testcase_count()
        # 发送通知
        notification_mapping = {
            NotificationType.EMAIL.value: SendEmail(allure_data).send_main,
            NotificationType.WECHAT.value: WeChatSend(allure_data).send_wechat_notification,
            NotificationType.DING_TALK.value: DingTalkSendMsg(allure_data).send_ding_notification,
            NotificationType.FEI_SHU.value: FeiShuTalkChatBot(allure_data).post
        }
        if config.notification_type != NotificationType.DEFAULT.value:
            notify_type = config.notification_type.split(',')
            for i in notify_type:
                notification_mapping.get(i)()
        # 启动allure服务
        os.system(f'allure serve {allure_result_path} -h  127.0.0.1 -p 9999 ')
        # 移除生成的文件
        shutil.rmtree(ensure_path_sep("\\file\\image\\screen_image"))
    # 发送测试结果

    except Exception:
        print('异常问题----')
        # 遇到异常情况发送邮箱
        # e = traceback.format_exc()
        # send_email = SendEmail(AllureDataCollect.get_testcase_count())
        # send_email.error_mail(e)
        raise


if __name__ == '__main__':
    run()

