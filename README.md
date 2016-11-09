# topn

## 在mongo中需要设置索引的主键有

'''python  
        # xmly qt kl 类似下面的部分需要设置索引
        audio = self.db[item.collection].find_one(
            {
                'album_id':item['album_id'],
                'id':item['id']
            }
        )
        db['daily'].update(
            {
                'key':'xmly_audio',
                'day':self.now
            },
            {
                "$inc":{"crawledCount":1}
            },
            upsert = True
        )

'''
