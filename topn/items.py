# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TopnItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class XMLYAudio(scrapy.Item):
    '''
    对应喜马拉雅fm 中的音频内容，目的是规定音频中都有哪些字段
    前半部分的内容通过接口 http://www.ximalaya.com/tracks/13569779.json
    获得
    中间部分内容通过地址
    http://www.ximalaya.com/36327519/sound/11362725
    获得
    '''
    collection = 'xmly_audio'
    contentSource = 'www.ximalaya.com'
    s_type = 'xmly_audio'

    # 歌曲的id
    id = scrapy.Field()
    # 歌曲文件地址的三个连接
    play_path_64 = scrapy.Field()
    play_path_32 = scrapy.Field()
    play_path = scrapy.Field()

    duration = scrapy.Field()
    title = scrapy.Field()
    nickname = scrapy.Field()
    uid = scrapy.Field()
    upload_id = scrapy.Field()

    # 歌曲的封面的图片连接地址
    cover_url = scrapy.Field()
    cover_url_142 = scrapy.Field()
    # 如下字段是被删除的字段，因为 喜马拉雅的返回的数据也在一直改变
    # formatted_created_at = scrapy.Field()
    # 如下字段为发布的时间
    created_at = scrapy.Field()

    play_count = scrapy.Field()
    comments_count = scrapy.Field()
    shares_count = scrapy.Field()
    favorites_count = scrapy.Field()
    album_id = scrapy.Field()
    album_title = scrapy.Field()
    intro = scrapy.Field()
    # 如下字段也被删除
    # time_until_now = scrapy.Field()
    category_name = scrapy.Field()
    category_title = scrapy.Field()

    # 音频的标签内容
    tags = scrapy.Field()
