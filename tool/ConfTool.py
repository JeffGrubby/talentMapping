#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022-01-20 11:17
# @Author  : Jeffrain
# @Contact    : https://github.com/JeffGrubby
# @File    : confToll.py
# @Software: PyCharm
import json


class ConfTool(object):
    """
    json配置文件类
    """
    @staticmethod
    def load():
        """
        读取配置文件
        :return:
        """
        with open("../project.config.json") as json_file:
            data = json.load(json_file)
        return data

    @staticmethod
    def update(config):
        """
        更新配置文件
        :param config: 字典
        :return:
        """
        with open("../project.config.json", 'w') as json_file:
            # json_file.write(json.dumps(config, indent=4))
            json.dump(config, json_file, indent=4, ensure_ascii=False)
        return None


if __name__ == '__main__':
    ConfTool.load()
    # conf = {"test": 1, "test1":2}
    # confTool.update(config=conf)