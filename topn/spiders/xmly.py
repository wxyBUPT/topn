# -*- coding: utf-8 -*-
import scrapy
# e-mail : xywbutp@gmail.com
'''
每一个爬虫都设置为一个新的进程
用外部数据库记录爬取结果与爬虫状态
注意：目前没有保存cookie，如果以后遇到爬虫被封的情况使用如下办法解决

1、添加cookie
2、随机headers，随机ua
2、代理
'''
import datetime
import json
import sys

import requests
from scrapy.http import Request
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

from topn.util.urlgenerator import UrlGenerator
from topn.items import XMLYAudio

class XmlySpider(scrapy.Spider):

    name = "xmly"
    allowed_domains = ["ximalaya.com"]
    start_urls = (
        'http://www.ximalaya.com/',
    )

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
        "Connection": "keep-alive",
        "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        #"HOST":''
    }

    urlGenenator = UrlGenerator()
    urls = urlGenenator.get_xmly_urls()
    topn_n = urlGenenator.get_xmly_topn_n()

    def __init__(self,stats,*args,**kwargs):
        dispatcher.connect(
            self.spider_closed,signals.spider_closed
        )
        super(XmlySpider,self).__init__(*args,**kwargs)
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(crawler.stats,*args,**kwargs)
        spider._set_crawler(crawler)
        return spider

    def start_requests(self):
        for url in self.urls:
            self.logger.info(u"开始爬取 %s 的top%d",url,self.topn_n)
            yield Request(
                url + "?order=asc",
                callback=self.parse,
                headers=self.headers
            )

    def parse(self, response):
        category = response.css(
            '.detailContent_category > a:nth-child(1)'
        ).xpath('text()')[0].extract().lstrip(u'【').rstrip(u'】')
        self.stats.inc_value(u"category_%s_album"%category, 1, 0)

        album = response.css(
            ".detailContent_title > h1:nth-child(1)"
        ).xpath("text()")[0].extract()

        count = response.css('.albumSoundcount').xpath(
            "text()").extract()[0].lstrip(u'(').rstrip(')')
        count = int(count)
        self.logger.info(u"栏目 %s 共有%d个歌曲，需要抓取%d首歌曲"%(
            album, count, self.topn_n
        ))
        can_crawl_count = min(count,self.topn_n,100)
        self.stats.inc_value(u"category_%s_audio"%category,
                             can_crawl_count,
                             0
                             )

        tags = response.css('a.tagBtn2').xpath('span/text()').extract()
        audioCountsStr = response.css('.albumSoundcount').xpath('text()').extract()[0]
        audioCount = int(audioCountsStr[1:-1])

        audios = response.css("li[sound_id]")[:can_crawl_count]
        for s in audios:
            audio = XMLYAudio()
            try:
                a_id = s.xpath('@sound_id').extract()[0]
                created_at = s.xpath('div/div/span/text()').extract()[0]
                created_at = datetime.datetime.strptime(
                    created_at,"%Y-%m-%d"
                )
                audio["id"] = a_id
                audio["created_at"] = created_at
            except:
                self.logger.error("发生了一些错误，请查看")

            a_url = "http://www.ximalaya.com/tracks/%s.json"%(a_id)
            r = requests.get(a_url,headers = self.headers)
            inc = self.stats.inc_value
            inc(
                'requests/request_count',
                1,
                0
            )
            inc(
                'requests/request_method_count/GET',
                1,
                0
            )
            inc(
                'requests/response_bytes',
                sys.getsizeof(r.text),
                0
            )
            inc(
                'requests/response_count',
                1,0
            )
            inc(
                'requests/response_status_count/%d'%r.status_code,
                1,
                0
            )
            inc(
                'audio_count',
                1,
                0
            )

            tmpDict = r.json()
            try:
                del tmpDict['discounted_price']
                del tmpDict['price']
                del tmpDict['id']
                del tmpDict['is_free']
                del tmpDict['waveform']
                del tmpDict['formatted_created_at']
                del tmpDict['is_favorited']
                del tmpDict['have_more_intro']
                del tmpDict['time_until_now']
                del tmpDict['played_secs']
                del tmpDict['is_paid']
            except:
                self.logger.error(u'发生了一些错误，请查看')
            audio.update(tmpDict)
            yield audio

        pass

    def inspect(self, response):
        from scrapy.shell import inspect_response
        inspect_response(response, self)

    def spider_closed(self,spider):
        stats = self.stats
        print dir(stats.get_stats())
        print type(stats.get_stats())
        print stats.get_stats()
        pass
