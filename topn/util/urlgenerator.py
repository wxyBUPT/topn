#coding=utf-8
from __future__ import absolute_import
__author__ = 'xiyuanbupt'
# e-mail : xywbupt@gmail.com

'''
负责产生爬虫爬取的所有网址，只负责和redis交互，从redis 中获得要爬取的top数目，要爬取的网站
'''
import logging
import logging.handlers

import redis

from ..conf import ConfUtil

class UrlGenerator:

    r = redis.StrictRedis(
        host=ConfUtil.get_redis_host(),
        port = ConfUtil.get_redis_port(),
        db = ConfUtil.get_redis_db()
    )

    def __init_logger(self):
        logger = logging.getLogger("topn_xmly")
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    def __init_urls(self):
        '''
        初始化当前爬取的url
        :return:
        '''
        self.xmly_urls = self.r.smembers(
            ConfUtil.get_xmly_topn_urls_key()
        )

    def __init__(self):
        '''
        初始化logger 和所有需要爬取的urls
        :return:
        '''
        self.logger = self.__init_logger()
        self.__init_urls()

    def get_xmly_urls(self):
        '''
        获得xmly要爬取的urls
        :return:
        '''
        return self.xmly_urls


if __name__ == "__main__":
    urlGenerator = UrlGenerator()

