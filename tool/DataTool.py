#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022-01-24 14:39
# @Author  : Jeffrain
# @Contact    : https://github.com/JeffGrubby
# @File    : DataTool.py
# @Software: PyCharm
import datetime

import pymysql
import hashlib
import time

from tool.ConfTool import ConfTool


class DataTool(object):
    """
    Mysql数据库操作类
    """
    def __init__(self):
        data = ConfTool.load()['mysql']
        self.conn = pymysql.connect(host=data['host'], port=data['port'], user=data['user'],
                             password=data['password'], database=data['database'][0], charset=data['charset'])
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def query_one(self, sql, args=None):
        """
        :param sql:sql语句
        :param args:参数列表，如元组、列表和字典
        :return:查询数据库一条数据
        """
        try:
            print("query_one {0} !".format(sql))
            self.cursor.execute(sql, args)
            self.conn.commit()
            return self.cursor.fetchone()
        except:
            print("query {0} failed!".format(sql))
            return None

    def query_all(self, sql, args=None):
        """
        :param sql:[select id,name from user where id=%s and name=%s]
        :param args:[('1','张三'),OR None]
        :return:返回查询的数据,args防止sql注入
        """
        try:
            print("query_all {0} !".format(sql))
            self.cursor.execute(sql, args)
            self.conn.commit()
            return self.cursor.fetchall()
        except:
            print("query {0} failed!".format(sql))
            return None

    def query(self, sql, args=None, one=False):
        """
        :param sql:sql语句
        :param args:参数列表，如元组、列表和字典
        :param one:one默认为False,执行query_all,否则执行query_one
        :return:mysql查询语句
        """
        if one:
            return self.query_one(sql, args)
        return self.query_all(sql, args)

    def close(self):
        """
        :return:关闭数据库连接
        """
        # 关闭游标
        self.cursor.close()
        # 断开数据库连接
        self.conn.close()


def makeMd5(mstr):
    """
    :param mstr:
    :return:生成md5
    """
    hmd5 = hashlib.md5()
    hmd5.update(mstr.encode("utf-8"))
    return hmd5.hexdigest()


def getTime():
    """
    :return:unix时间戳
    """
    return round(time.time())


def timeFormat(timestamp):
    """
    :param timestamp:
    :return:时间格式化
    """
    # return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
    # return datetime.fromtimestamp(timestamp)
    return datetime.datetime.utcfromtimestamp(timestamp)


if __name__ == '__main__':
    db = DataTool()
    sql = 'select * from test'
    print(db.query(sql))
    db.close()
