# -*- coding: utf-8 -*-
import scrapy
# e-mail : xywbutp@gmail.com

from topn.conf import ConfUtil

class XmlySpider(scrapy.Spider):
    ConfUtil.get_xmly_topn_key()
    name = "xmly"
    allowed_domains = ["ximalaya.com"]
    start_urls = (
        'http://www.ximalaya.com/',
    )

    def parse(self, response):

        pass

    def inspect(self, response):
        from scrapy.shell import inspect_response
        inspect_response(response, self)
