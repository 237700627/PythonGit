# -*- coding:UTF-8 -*- 
# Author:hanbo(Portos)
# Datetime:2019/2/19 9:47
# Project:PyCharmPro
import os
import sys
sys.path.append("../src")
sys.path.append("..")
from config import sendemail
from utils.sendEmail import *
# from src.httprunner.api import HttpRunner
from src.httprunner.api import HttpRunner
runner = HttpRunner()

# discover_cases = os.path.join(r'testcases', 'pc_auditTask_case.yaml')
# discover_cases = os.path.join(r'testsuites', 'core_business_suite.yaml')
# discover_cases = os.path.join(r'testsuites', 'cancel_order_suite.yaml')
# discover_cases = os.path.join(r'testsuites', 'abnormal_business_suite.yaml')
#discover_cases = os.path.join(r'testsuites', 'single_pc_suite.yaml')


discover_cases = os.path.join(r'testsuites')
discover_cases = os.path.abspath(discover_cases)

print(discover_cases)

result = runner.run(discover_cases)
summary = runner.summary
if sendemail == 1:
    receivers = ['subing@cias.cn','liujun@cias.cn','quyong@cias.cn','qiucaixia@cias.cn',]
    total = summary['stat']['testcases']['total']
    success = summary['stat']['testcases']['success']
    fail = summary['stat']['testcases']['fail']
    url = 'http://10.3.200.99/autotest/injury_api_autotest/reports' + result.split('reports')[-1]
    print(url)
    html = """
    <html>
      <head></head>
      <body>
        <p>你好！<br>
           本次自动化执行测试结果为：
           执行用例数量：%s，
           成功数量：%s，
           失败数量：%s，<br>
           查看详细内容请 <a href=%s>点击</a><br>
        </p>
      </body>
    </html>
    """ % (total, success, fail, url)

    email = SendEmail(receivers, '人伤项目')
    email.sendemail(html, 'html')