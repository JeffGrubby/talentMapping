#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/1/6 10:22
# @Author  : Jeffrain
# @Contact    : https://github.com/JeffGrubby
# @File    : Enterprise.py
# @Software: PyCharm
import json
import time
import requests
import math
from multiprocessing import Pool, cpu_count
import pymysql
import tqdm
# TODO 引入协程应用加速爬取：gevent
# TODO 引入布隆过滤器做网址去重
# TODO 增加IP代理池
from tool.ConfTool import ConfTool


class MyData(object):
    """
    数据库操作
    """
    def __init__(self):
        """
        mysql设置
        """
        data = ConfTool.load()['mysql']
        self.db = pymysql.connect(host=data['host'], port=data['port'], user=data['user'],
                                  password=data['password'], database=data['database'][0], charset=data['charset'])
        self.cursor = self.db.cursor()
        self.sql = 'insert into canenterprise(ENTNAME, USCC, candate, PAGENO, pripid, REGNO)' \
                   ' values(%s, %s, %s, %s, %s, %s)'

    def execute_sql(self, result):
        '''
        mysql数据插入
        :return:
        '''
        try:
            for res in result:
                self.cursor.execute(self.sql, (res['ENTNAME'], res['USCC'], res['candate'], res['PAGENO'], res['pripid'], res['REGNO']))
                self.db.commit()
        except Exception as e:
            print(e)

    def quit_sql(self):
        '''
        关闭mysql连接
        :return:
        '''
        self.cursor.close()
        self.db.commit()
        self.db.close()


class CanEnterprise:
    """
    注销企业信息/企业注销信息（更详细）
    接口限制为每页请求200条记录
    """
    def __init__(self):
        # 接口授权设置
        self.header = ConfTool.load()['request']['header']
        self.proxy = ConfTool.load()['request']['proxies']
        self.secret = ConfTool.load()['secret']
        self.num_url = 'http://data.zjzwfw.gov.cn/jdop_front/interfaces/cata_19295/get_total.do?appsecret={0}'.\
            format(self.secret)
        self.num = requests.get(self.num_url).json()['data']
        print('total num:', self.num)
        self.page_size = math.ceil(self.num / 200)
        print('total page:', self.page_size)
        self.list_len = list(range(31350, self.page_size+1))
        # 200页测试用
        # self.list_len = list(range(1, 201))

    # requests串行调用接口
    def req(self):
        start = time.time()
        result = []
        for i in self.list_len:
            data_url = 'http://data.zjzwfw.gov.cn/jdop_front/interfaces/cata_19295/get_data.do?pageNum={0}&' \
                       'pageSize=200&appsecret={1}'.format(i, self.secret)
            content = requests.get(data_url, allow_redirects=False, headers=self.header).json()['data']
            for j in range(0, len(content)):
                if u'青田' in content[j]['ENTNAME']:
                    content[j]['PAGENO'] = i
                    result.append(content[j])
            MyData().execute_sql(result)

        print('requests time:',  time.time()-start)

    # Pool多进程并行调用接口
    def pro(self, page_idx):
        """
        接口调用
        :param page_idx:页面序号
        :return:
        """
        data_url = 'http://data.zjzwfw.gov.cn/jdop_front/interfaces/cata_19295/get_data.do?pageNum={0}&' \
                   'pageSize=200&appsecret={1}'.format(page_idx, self.secret)
        print(data_url)
        contents = requests.get(data_url, allow_redirects=False, headers=self.header, timeout=30,
                                proxies=self.proxy).json()['data']
        result = []
        # print("page index: ", page_idx)
        for content in contents:
            if u'青田' in content['ENTNAME']:
                content['PAGENO'] = page_idx
                result.append(content)

        print('result: ', len(result))
        MyData().execute_sql(result)

    def pool_req(self):
        """
        进程池爬取
        :return:
        """
        start = time.time()
        with Pool(cpu_count()) as p:
            r = list(tqdm.tqdm(p.map(self.pro, self.list_len), total=len(self.list_len)))
        # pool = Pool(cpu_count())
        # pool.map(self.pro, self.list_len)
        # pool.close()
        # pool.join()
        MyData().quit_sql()
        print('Pool time:', time.time()-start)


if __name__ == '__main__':
    test = CanEnterprise()
    # test.req()
    test.pool_req()

