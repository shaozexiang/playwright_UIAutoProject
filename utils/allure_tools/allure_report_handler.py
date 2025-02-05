# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : allure_report_handler.py
@Time : 2025/2/5 23:14
"""
import json
import os.path

import yaml

from utils import config
from utils.other_tools.get_file_path import ensure_path_sep


class AllureReportHandler:
    """
    美化allure报告
    """

    def __init__(self, allure_html_path, allure_result_path):
        """
        allure_html_path: allure生成报告的目录
        allure_result_path: allure保存测试结果目录
        """
        # allure_html_path = ensure_path_sep("\\output\\report\\html")
        # allure_result_path = ensure_path_sep("\\output\\report\\tmp")
        if os.path.exists(allure_result_path) and os.path.exists(allure_html_path):
            self.allure_result_path = allure_result_path
            self.allure_html_path = allure_html_path
        else:
            print(f"allure results以及allure html报告未生成~ \n"
                  f"allure报告生成依赖java环境，请检查运行环境是否正确安装JDK环境\n"
                  f"allure_results_path={allure_result_path}， allure_html_path={allure_html_path}\n")
            raise "allure results以及allure html报告未生成~！\nallure报告生成依赖java环境，请检查运行环境是否正确安装JDK环境\nallure_results_path={allure_results_path}， allure_html_path={allure_html_path}\n"

    def set_windows_title(self, title_name):
        """
        更改网页的名称
        :param title_name: 自定义的标题名称
        :return:
        """
        title_path = os.path.join(self.allure_html_path, 'index.html')
        with open(title_path, 'r+', encoding='utf-8') as file:
            all_lines = file.readlines()
            file.seek(0)
            file.truncate()
            for line in all_lines:
                file.write(line.replace("Allure Report", title_name))

            file.close()

    def set_report_name(self, report_name):
        """
        更改allure报告的默认标题名称
        :param report_name: 新的报告名称
        :return:
        """
        report_path = os.path.join(self.allure_html_path, 'widgets', 'summary.json')
        with open(report_path, 'r+', encoding='utf-8') as file:
            summary_json: dict = json.load(file)
            summary_json['reportName'] = report_name

        with open(report_path, 'w') as file:
            json.dump(summary_json, file, indent=4)

    def set_report_env_on_html(self, env_info: dict):
        """
        写入环境变量
        :param env_info:
        :return:
        """
        envs = []
        for k, v in env_info.items():
            envs.append({
                "name": k,
                "value": [v]
            })
        with open(os.path.join(self.allure_html_path, "widgets", "environment.json"), 'w', encoding="utf-8") as f:
            json.dump(envs, f, ensure_ascii=False, indent=4)


def generate_allure_report(**kwargs):
    """
    生成allure报告
    :param kwargs:
    :return:
    """
    # config_path = ensure_path_sep("\\config\\config.yaml")
    # with open(config_path, 'r', encoding='utf-8') as file:
    #     config_data = yaml.safe_load(file)
    #     file.close()
    kwargs.get('')
    # 判断为不同的运行平台执行不同的allure命令
    allure_report = AllureReportHandler()
    # 设置报告窗口的标题
    allure_report.set_windows_title(
        title_name=config.common.project_name
        # title_name=config_data['common']['project_name']
    )
    # 设置allure报告的Overview名称
    allure_report.set_report_name(
        report_name=config.common.report_name
        # report_name=config_data['common']['report_name']
    )

    # 设置环境
    allure_report.set_report_env_on_html(
        env_info=config.common.env
        # env_info=config_data['common']['env']
    )


if __name__ == '__main__':
    # AllureReportHandler().set_report_name('test_reportName')
    generate_allure_report()

