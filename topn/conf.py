#coding=utf-8
__author__ = 'xiyuanbupt'
# e-mail : xywbupt@gmail.com

'''
配置中心，虽然代码很麻烦，但是省去后续配置的变更
'''

import ConfigParser
import redis

cf = ConfigParser.ConfigParser()
cf.read('global.ini')

r = redis.StrictRedis(
    host=cf.get("redis","host"),
    port = cf.get("redis","port"),
    db = cf.get("redis","db")
)

class ConfUtil:

    '''
    设置爬虫和管理后端共有的配置中心，虽然代码量比较大，逻辑比较多
    但是相对于使用Celery 等队列任务来说减少了不小学习成本
    '''

    cnr_conf_hash = cf.get("cnr_conf","hash_name")

    @classmethod
    def get_cnr_conf_hash(cls):
        '''
        获得conf hash表名
        :return:
        '''
        return cls.cnr_conf_hash

    @classmethod
    def get_xmly_topn_key(cls):
        '''
        获得保存topn_n n 的数目的key
        :return:
        '''
        return r.hget(
            cls.cnr_conf_hash,cf.get(
                "cnr_conf","xmly_top_n"
            )
        )

    @classmethod
    def get_xmly_topn_urls_key(cls):
        '''
        获得保存xmly所有urls 的key
        :return:
        '''
        return r.hget(
            cls.cnr_conf_hash,
            cf.get(
                "cnr_conf", "xmly_topn_urls"
            )
        )

    # 从配置中心中获得key
    @classmethod
    def get_xmly_topn_table_key(cls):
        '''
        获得本次爬取xmly topn 保存的table的key值
        :return:
        '''
        return r.hget(
            cls.cnr_conf_hash,
            cf.get(
                "cnr_conf","xmly_topn_table"
            )
        )

    @classmethod
    def get_xmly_topn_table(cls):
        return r.get(cls.get_xmly_topn_table_key())

    # 设置配置中心xmlytopntable key 的值
    @classmethod
    def set_xmly_topn_table_key(cls, key):
        r.hset(
            cls.cnr_conf_hash,
            cf.get(
                "cnr_conf", "xmly_topn_table"
            ),
            key
        )

    @classmethod
    def get_topn_report_table_name(cls):
        '''
        获得存储table
        :return:
        '''
        return r.get(cls.get_topn_report_table_key())

    @classmethod
    def get_topn_report_table_key(cls):
        return r.hget(
            cls.cnr_conf_hash,
            cf.get(
                "cnr_conf","topn_report_table"
            )
        )

    @classmethod
    def set_topn_report_table_key(cls,key):
        r.hset(
            cls.cnr_conf_hash,
            cf.get(
                "cnr_conf","topn_report_table",
            ),
            key
        )


    @classmethod
    def set_xmly_topn_key(cls,key):
        r.hset(
            cls.cnr_conf_hash,
            cf.get(
                "cnr_conf","xmly_top_n",
            ),
            key
        )

    @classmethod
    def set_xmly_topn_urls_key(cls,key):
        r.hset(
            cls.cnr_conf_hash,
            cf.get("cnr_conf","xmly_topn_urls"),
            key
        )

    @classmethod
    def xmly_album_table(cls):
        return cf.get("mongo","xmly_album")

    @classmethod
    def xmly_audio_table(cls):
        return cf.get("mongo","xmly_audio")

    @classmethod
    def xmly_category_table(cls):
        return cf.get("mongo","xmly_category")

    @classmethod
    def get_redis_host(cls):
        return cf.get("redis","host")

    @classmethod
    def get_redis_port(cls):
        return cf.getint("redis", "port")

    @classmethod
    def get_redis_db(cls):
        return cf.getint("redis", "db")

    @classmethod
    def get_mongo_uri(cls):
        return cf.get('mongo','uri')

    @classmethod
    def get_mongo_db(cls):
        return cf.get('mongo','db')