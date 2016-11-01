# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
import uuid

import pymongo

from topn.conf import ConfUtil

class TopnPipeline(object):
    def process_item(self, item, spider):
        return item

class SaveToMongo(object):

    def __init__(self):
        self.mongo_uri = ConfUtil.get_mongo_uri()
        self.mongo_db = ConfUtil.get_mongo_db()
        self.now = None


    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self,spider):
        self.client.close()

    def process_item(self,item,spider):
        # 将每天爬取的数量保存到mongo中
        dt = datetime.datetime.now()
        self.now = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        # 将具体的数据保存到 mongo 中
        s_type = item.s_type
        if s_type == 'xmly_audio':
            self._saveXMLYAudio(item)
        elif s_type == 'xmly_album':
            self._saveXMLYAlbum(item)
        elif s_type == 'kl_audio':
            self._saveKLAudio(item)
        elif s_type == 'kl_album':
            self._saveKlAlbum(item)
        elif s_type == 'qt_item':
            self._saveQTAlbum(item)
        elif s_type == 'qt_audio':
            self._saveQTAudio(item)
        else:
            self.db[s_type].insert(dict(item))

    def _saveQTAlbum(self,item):
        self.db['daily'].update(
            {
                'key':'qt_album',
                'day':self.now
            },
            {
                "$inc":{"crawledCount":1}
            },
            upsert=True
        )
        album = self.db[item.collection].find_one(
            {
                "category":item["category"],
                "subcategory":item["subcategory"],
                "albumName":item["albumName"]
            }
        )
        if album:
            self.db[item.collection].update(
                {
                    "_id":album['_id']
                },
                {
                    "$inc":{"crawledCount":1}
                }
            )
        else:
            tmp = dict(item)
            tmp['crawledCount'] = 1
            tmp['crawledTime'] = datetime.datetime.now()
            self.db[item.collection].insert(
                tmp
            )
        return item

    def _saveQTAudio(self,item):
        self.db['daily'].update(
            {
                'key':'qt_audio',
                'day':self.now
            },
            {
                "$inc":{"crawledCount":1}
            },
            upsert = True
        )
        audio = self.db[item.collection].find_one(
            {
                "audioName":item["audioName"],
                "playUrl":item["playUrl"]
            }
        )
        if audio:
            self.db[item.collection].update(
                {
                    "_id":audio["_id"]
                },
                {
                    "$inc":{"crawledCount":1}
                }
            )
        else:
            tmp = dict(item)
            tmp['crawledCount'] = 1
            tmp['uuid'] = uuid.uuid1().hex
            tmp['crawledTime'] = datetime.datetime.now()
            tmp['sendToCNRTime'] = None
            tmp['audioDownloadDir'] = None
            self.db[item.collection].insert(
                tmp
            )
        return item

    def _saveKLAudio(self,item):
        self.db['daily'].update(
            {
                'key':'kl_audio',
                'day':self.now
            },
            {
                "$inc":{"crawledCount":1}
            },
            upsert = True
        )
        #以audioId 与 playUrl 为主键更新或者插入数据
        audio = self.db[item.collection].find_one(
                {
                    'audioId':item["audioId"],
                    'playUrl':item['playUrl']
                }
        )
        if audio:
            self.db[item.collection].update(
                {
                    "_id":audio['_id']
                },
                {
                    "$inc":{"crawledCount":1},
                    "$set":dict(
                        likedNum = item['likedNum'],
                        listenNum = item['listenNum'],
                        commentNum = item['commentNum']
                    )
                }
            )
        else:
            tmp = dict(item)
            tmp['crawledCount'] = 1
            tmp['uuid'] = uuid.uuid1().hex
            tmp['crawledTime'] = datetime.datetime.now()
            tmp['sendToCNRTime'] = None
            tmp['audioDownloadDir'] = None
            self.db[item.collection].insert(
               tmp
            )
        return item

    def _saveKlAlbum(self,item):
        self.db['daily'].update(
            {
                'key':'kl_album',
                'day':self.now
            },
            {
                "$inc":{"crawledCount":1}
            },
            upsert = True
        )
        album = self.db[item.collection].find_one(
            {
                'categoryId':item['categoryId'],
                'albumId' : item['albumId']
            }
        )
        #更新本专辑被爬取的次数
        if album:
            self.db[item.collection].update(
                {
                    '_id':album['_id']
                },
                {
                    '$inc':{'crawledCount':1},
                    '$set':dict(item)
                }
            )
        else:
            tmp = dict(item)
            tmp['crawledCount'] = 1
            tmp['crawledTime'] = datetime.datetime.now()
            self.db[item.collection].insert(
                dict(item)
            )
        return item

    def _saveXMLYAudio(self,item):

        # topn 爬取同样记录到mongo 中，次操作为mongo 其实次操作对mongo 造成巨大的压力
        # 但是之前就是这么设计的没有办法
        self.db['daily'].update(
            {
                'key':'xmly_audio',
                'day':self.now
            },
            {
                "$inc":{"crawledCount":1}
            },
            upsert = True
        )

        # 当前设计是将爬取到的数据插入到大表中
        audio = self.db[item.collection].find_one(
            {
                'album_id':item['album_id'],
                'id':item['id']
            }
        )
        if not audio:
            tmp = dict(item)
            tmp['crawledCount'] = 1
            tmp['uuid'] = uuid.uuid1().hex
            tmp['crawledTime'] = datetime.datetime.now()
            tmp['audioDownloadDir'] = None
            tmp['sendToCNRTime'] = None
            tmp['audioChecksum'] = None
            self.db[item.collection].insert(tmp)
        else:
            self.db[item.collection].update(
                {
                    '_id':audio['_id']
                },

                {
                    "$inc":{'crawledCount':1},
                    "$set":dict(item)
                }
            )

        # 下面操作是为了将新的topn 保存到新的表中
        # 这种操作比较坑人，之后可以优化
        audio = self.db[item.collection].find_one(
            {
                'album_id':item['album_id'],
                'id':item['id']
            }
        )
        self.db[ConfUtil.get_xmly_topn_table()].update(
            {
                "_id":audio["_id"],
            },
            audio,
            upsert =True
        )
        return item

    def _saveXMLYAlbum(self,item):
        self.db['daily'].update(
            {
                'key':'xmly_album',
                'day':self.now
            },
            {
                "$inc":{"crawledCount":1}
            },
            upsert = True
        )
        album = self.db[item.collection].find_one(
            {
                'album_id':item['album_id']
            }
        )
        if not album:
            tmp = dict(item)
            tmp['crawledCount'] = 1
            tmp['crawledTime'] = datetime.datetime.now()
            self.db[item.collection].insert(tmp)
        else:
            self.db[item.collection].update(
                {
                    '_id':album['_id'],
                },
                {
                    '$inc':{'crawledCount':1},
                    "$set":dict(item)
                }
            )
        return item