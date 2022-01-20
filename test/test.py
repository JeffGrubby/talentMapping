#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022-01-20 10:04
# @Author  : Jeffrain
# @Contact    : https://github.com/JeffGrubby
# @File    : test.py
# @Software: PyCharm
import requests

proxy = {
    'http': 'http://125.74.93.60:8083'
}
# res = requests.get("http://httpbin.org/ip")
res = requests.get("http://httpbin.org/ip", proxies=proxy)
print(res.text)

