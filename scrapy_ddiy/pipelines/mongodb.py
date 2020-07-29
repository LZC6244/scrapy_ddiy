# -*- coding: utf-8 -*-
"""
MongoDB Pipeline
"""

import logging
import pymongo
from itemadapter import ItemAdapter
from pymongo.errors import BulkWriteError

logger = logging.getLogger(__name__)


class MongodbPipeline(object):
    mongo_coll: pymongo.collection.Collection

    def __init__(self, mongo_uri, mongo_db, mongo_params, bulk_insert):
        self.mongo_db = mongo_db
        self.bulk_insert = bulk_insert
        self.mongo_cli = pymongo.MongoClient(mongo_uri, **mongo_params)
        # 用于临时保存数据的列表
        self.data_li = []

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'scrapy_ddiy_test'),
            mongo_params=crawler.settings.getdict('MONGO_PARAMS', {}),
            bulk_insert=crawler.settings.getint('BULK_INSERT', 5)
        )

    def open_spider(self, spider):
        mongo_coll = getattr(spider, 'table_name_mongo', None) or \
                     getattr(spider, 'table_name_ddiy', None) or \
                     spider.name
        self.mongo_coll = self.mongo_cli[self.mongo_db][mongo_coll]

    def close_spider(self, spider):
        if self.data_li:
            self.insert_data(spider, self.data_li)
        self.mongo_cli.close()

    def insert_data(self, spider, data_li: list):
        try:
            self.mongo_coll.insert_many(data_li, ordered=False)
        except BulkWriteError as e:
            # 插入重复数据（_id）时会报此错误
            pass
        self.data_li.clear()
        logger.info(f'Bulk insert {len(data_li)} items successfully')

    def process_item(self, item, spider):
        data = ItemAdapter(item).asdict()
        self.data_li.append(data)
        if len(self.data_li) >= self.bulk_insert:
            self.insert_data(spider, self.data_li)
        return item
