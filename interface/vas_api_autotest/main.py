# -*- coding:UTF-8 -*- 
# Author:hanbo(Portos)
# Datetime:2019/5/25 17:31
# Project:PyCharmPro
import os

from src.httprunner.api import HttpRunner


# 执行所有接口用例
def run_test_cases():
    runner = HttpRunner()
    test_cases = os.path.join('testcases/single_case/manage/right', 'list.yaml')
    test_cases = os.path.abspath(test_cases)
    runner.run(test_cases)
    return True


if __name__ == '__main__':
    run_test_cases()
