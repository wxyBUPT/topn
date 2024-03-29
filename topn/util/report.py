#coding=utf-8
__author__ = 'xiyuanbupt'
# e-mail : xywbupt@gmail.com

import pymongo
import xmlrpclib

from topn.conf import ConfUtil

'''
本部分负责产生报表，即将某时刻产生的topn报表保存到mongo 中

报表存储在存储在数据库固定的表中，
'''
# 创建到mongo 的连接
mongo_uri = ConfUtil.get_mongo_uri()
db_name = ConfUtil.get_mongo_db()
client = pymongo.MongoClient(mongo_uri)


def write_xmly_status(status):
    '''
    一个xmly 的爬取进程只在一个进程执行一次，
    将status 保存到mongo
    :param status:
    :return:
    '''

    db = client[db_name]

    # 保存status，并添加其他的必要信息
    report = {"status":status}
    report['table'] = ConfUtil.get_xmly_topn_table()
    report['table_delete'] = False
    report['s_type'] = 'xmly_audio'
    db[ConfUtil.get_topn_report_table_name()].insert(
        report
    )

def write_qt_status(status):
    '''
    保存qt 爬取状态
    :param status:
    :return:
    '''

    db = client[db_name]

    report = {"status":status}
    report['s_type'] = 'qt_topn'
    db[ConfUtil.get_topn_report_table_name()].insert(
        report
    )
