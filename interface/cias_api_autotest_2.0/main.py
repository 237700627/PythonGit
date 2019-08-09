#!/usr/bin/python
# coding:utf-8
# Author:hanbo(Portos)
# Datetime:2019/4/23 15:33
# Project:PyCharmPro
"""
使用说明：
本脚本用于批量执行接口自动化脚本
"""

import os
import sys
sys.path.append("../src")
sys.path.append("..")
from src.httprunner.api import HttpRunner



runner = HttpRunner()
# discover_cases = os.path.join('testcases/close_transfer', 'close_transfer_parttime_working_process.yaml')
discover_cases = os.path.join('testcases/docking_dispatch', 'docking_parttime_working_process.yaml')
# discover_cases = os.path.join('testcases/docking_dispatch', 'docking_process.yaml')

discover_cases = os.path.abspath(discover_cases)
# print(discover_cases)
runner.run(discover_cases)
