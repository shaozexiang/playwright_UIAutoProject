# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : allure_report_data.py
@Time : 2025/2/5 23:14
"""
import json
from typing import List, Text

from utils.other_tools.get_file_path import  ensure_path_sep
from utils.other_tools.get_file_path import get_all_path
from utils.other_tools.models import TestMetrics

'''
返回
'''


class AllureDataCollect:
    """
    收集allure报告中的数据用于发送报告
    """

    @classmethod
    def get_testcase(cls) -> List:
        testcase_path = ensure_path_sep("\\output\\report\\html\\data\\test-cases")
        testcase = []
        for i in get_all_path(testcase_path):
            with open(i, 'r', encoding='utf-8') as file:
                data = json.load(file)
                testcase.append(data)

        return testcase

    def get_failed_data(self) -> List:
        testcase_data = self.get_testcase()
        error_case_data = []
        for i in testcase_data:
            if i['status'] == 'broken' or i['status'] == 'failed':
                error_case_data.append((i['name'], i['fullName']))
        return error_case_data

    def get_failed_data_detail(self) -> Text:
        """
        获取失败用例的名称和全类限定名
        :return:
        """
        failed_case = self.get_failed_data()
        values = ""
        if len(failed_case) > 0:
            values += "失败用例************\n"
            for i in failed_case:
                values += "        " + i[0] + ":" + i[1] + "\n"
        return values

    @classmethod
    def get_testcase_count(cls) -> "TestMetrics":
        """
        计算用例执行的成功率,便于邮件输出信息
        :return:
        """
        try:
            with open(ensure_path_sep("\\output\\report\\html\\widgets\\summary.json")) as file:
                json_data = json.load(file)
                _case_count = json_data['statistic']
                _time = json_data['time']
                stat_keys = ['failed', 'broken', 'skipped', 'passed', 'total']
                run_case_data = {key: value for key, value in _case_count.items() if key in stat_keys}
                if run_case_data['total'] > 0:
                    run_case_data['pass_rate'] = round(run_case_data['passed'] / run_case_data['total'] * 100, 2)
                else:
                    run_case_data['pass_rate'] = 0.0
                run_case_data['time'] = run_case_data['time'] = 0 if run_case_data['total'] == 0 else round(
                    _time['duration'] / 1000, 2)
                run_case_data['time'] = str(run_case_data['time'])
                run_case_data['time'] += "s"
                return TestMetrics(**run_case_data)
        except FileNotFoundError as exc:
            raise FileNotFoundError(
                "未找到生成的allure报告，请检查路径是否正确"
            ) from exc


if __name__ == '__main__':
    testcase_data = AllureDataCollect().get_failed_data_detail()
    print(testcase_data)


