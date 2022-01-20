#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/1/10 14:22
# @Author  : Jeffrain
# @Contact    : https://github.com/JeffGrubby
# @File    : Enterprise.py
# @Software: PyCharm
import re
import urllib.parse
import requests
import pymysql

from tool.ConfTool import ConfTool


class Enterprise:
    def __init__(self):
        self.url_prefix = 'https://aiqicha.baidu.com/s?t=0&q='
        self.header = ConfTool.load()['request']['header']
        res = requests.get('https://aiqicha.baidu.com/', headers=self.header)
        # cookies = dict_from_cookiejar(res.cookies)
        self.session = requests.Session()
        self.session.cookies = res.cookies

        self.sql = 'insert into enterprise(entName, regNo, legalPerson, openStatus, startDate, district, regCapital,' \
                   'paidinCapital, entType, industry, regCode, orgNo, taxNo, qualification, openTime, annualDate, authority,' \
                   'prevEntName, regAddr, latlong, scope) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,' \
                   '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    def req(self, key):
        """
        模拟aiqicha首页键入文本请求获取详情页面参数
        :param key:企业名称(建议全称)
        :return:
        """
        url = self.url_prefix + urllib.parse.quote(key)
        self.header['Referer'] = url
        print(url)
        response = self.session.get(url, headers=self.header).text
        match_obj = re.search(r'pid":"(\d+)"', response)
        print(match_obj)
        if match_obj:
            pid = match_obj.group(1)
            print(pid)
            self.enterprise_data(pid)
        else:
            print('None')

    def enterprise_data(self, pid):
        """
        请求企业基本信息数据
        :param pid:企业详情页面ID
        :return:
        """
        url = 'https://aiqicha.baidu.com/detail/basicAllDataAjax?pid={0}'.format(pid)
        self.header['Referer'] = 'https://aiqicha.baidu.com/company_detail_{0}'.format(pid)
        # print(url)
        # print(self.header)
        response = self.session.get(url, headers=self.header)
        data = response.json()['data']
        # print(data)
        self.basic_data(data['basicData'])

    def basic_data(self, basicdata):
        """
        解析JSON结果并保存至数据库
        :param basicdata:请求返回结果
        :return:
        """
        entName = basicdata['entName']
        regNo = basicdata['regNo']
        legalPerson = basicdata['legalPerson']
        openStatus = basicdata['openStatus']
        startDate = basicdata['startDate']
        district = basicdata['district']
        regCapital = basicdata['regCapital']
        paidinCapital = basicdata['paidinCapital']
        entType = basicdata['entType']
        industry = basicdata['industry']
        regCode = basicdata['regCode']
        orgNo = basicdata['orgNo']
        taxNo = basicdata['taxNo']
        qualification = basicdata['qualification']
        openTime = basicdata['openTime']
        annualDate = basicdata['annualDate']
        authority = basicdata['authority']
        prevEntName = basicdata['prevEntName']
        regAddr = basicdata['regAddr']
        latlong = self.get_lat_long(regAddr)
        scope = basicdata['scope']

        data = ConfTool.load()['mysql']
        db = pymysql.connect(host=data['host'], port=data['port'], user=data['user'],
                                  password=data['password'], database=data['database'][0], charset=data['charset'])
        cursor = db.cursor()
        cursor.execute(self.sql, (entName, regNo, legalPerson, openStatus, startDate, district, regCapital,
                   paidinCapital, entType, industry, regCode, orgNo, taxNo, qualification, openTime, annualDate,
                   authority,prevEntName, regAddr, latlong, scope))
        db.commit()
        cursor.close()
        db.close()

    def get_lat_long(self, address):
        """
        地址转换经纬度
        :param address:中文地址
        :return:
        """
        url = 'http://api.map.baidu.com/geocoder?output=json&address={0}'.format(urllib.parse.quote(address))
        result = self.session.get(url, headers=self.header).json()['result']['location']
        if result:
            return '{0},{1}'.format(result['lng'], result['lat'])
        else:
            return None


if __name__ == '__main__':
    ent = Enterprise()
    ent.req(u'网易')