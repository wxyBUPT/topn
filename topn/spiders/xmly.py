# -*- coding: utf-8 -*-
import scrapy


class XmlySpider(scrapy.Spider):
    name = "xmly"
    allowed_domains = ["ximalaya.com"]
    start_urls = (
        'http://www.ximalaya.com/',
    )

    def parse(self, response):

        pass
