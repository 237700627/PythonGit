# -*- coding:UTF-8 -*-
# Author:subing
# Datetime:2019/2/28
"""
函数说明：
1、本方法功能为提供从文件中获取文件内容转换为对应的内容，入参为文件名称
2、Loadjsondata函数将json文件中的内容转换为json格式内容
"""
import json
import os
import sys
class Loaddata():

    @staticmethod
    def Loadjsondata(filename):
        filepath = os.path.join("data",filename)
        with open(filepath, "r", encoding='utf-8') as f:
            loaddata = json.load(f)
            return loaddata


