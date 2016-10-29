#coding=utf-8
__author__ = 'xiyuanbupt'
# e-mail : xywbupt@gmail.com
'''
脚本由于初始化测试环境

本脚本非常重要，为前后端
'''

import ConfigParser

import redis
import pymongo

from topn.conf import ConfUtil

cf = ConfigParser.ConfigParser()
cf.read('global.ini')

r = redis.StrictRedis(
    host = cf.get("redis","host"),
    port = cf.get("redis","port"),
    db = cf.get("redis","db")
)

client = pymongo.MongoClient(ConfUtil.get_mongo_uri())
db = client[ConfUtil.get_mongo_db()]

def conf_conf():
    '''
    下面是初始化配置中心，整个项目的所有配置都在这里初始化
    :return:
    '''
    ConfUtil.set_xmly_topn_key("xmly_topn_n")
    ConfUtil.set_xmly_topn_urls_key("xmly_topn_albums_url")

def set_test_env():
    '''
    设置测试环境
    :return:
    '''
    # 设置喜马拉雅的测试环境，在redis 中随机抽取10个网址，爬取top100 的节目
    res = db.get_collection(ConfUtil.xmly_album_table()).find().limit(10)

    urls = [
        album["href"] for album in res
    ]

    top_n = 100

    r.set(ConfUtil.get_xmly_topn_key(), top_n)
    print u'在这里'
    print ConfUtil.get_xmly_topn_key()
    print r.get(ConfUtil.get_xmly_topn_key())
    print urls[0]
    print ConfUtil.get_xmly_topn_urls_key()
    r.sadd(ConfUtil.get_xmly_topn_urls_key(),urls[0])
    r.sadd(ConfUtil.get_xmly_topn_urls_key(), *urls)
    print r.smembers(ConfUtil.get_xmly_topn_urls_key())


if __name__ == "__main__":
    set_test_env()
