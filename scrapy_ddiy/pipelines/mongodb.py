# -*- coding: utf-8 -*-
"""
MongoDB Pipeline
"""
import re
import pymongo
from itemadapter import ItemAdapter
from pymongo.errors import BulkWriteError


class MongodbPipeline(object):
    mongo_coll: pymongo.collection.Collection

    def __init__(self, mongo_uri, mongo_db, mongo_params, mongo_index_dict, bulk_insert):
        self.mongo_db = mongo_db
        self.mongo_index_dict = mongo_index_dict
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
            mongo_index_dict=crawler.settings.getdict('MONGO_INDEX_DICT', {}),
            bulk_insert=crawler.settings.getint('BULK_INSERT', 5)
        )

    def open_spider(self, spider):
        mongo_coll = getattr(spider, 'table_name_ddiy', None) or spider.name
        self.mongo_coll = self.mongo_cli[self.mongo_db][mongo_coll]
        index_name_li = list(self.mongo_coll.index_information().keys())
        # 为 MongoDB 集合创建索引
        # 目前仅支持单字段索引，若要创建复合索引或进行其他复杂操作，请自行在 spider.custom_init 方法中执行
        for index_name, index_sort in self.mongo_index_dict.items():
            index_exists = False
            for i in index_name_li:
                if re.search(f'{index_name}_-?1', i):
                    index_name_li.remove(i)
                    index_exists = True
                    break
            if not index_exists:
                create_index = self.mongo_coll.create_index([(index_name, index_sort)])
                spider.logger.info(f'Created index => {create_index}')

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
        except Exception as e:
            # TODO: 重试插入x次后跳过该批数据，或者单条插入，出错时发送错误提醒邮件
            pass

        spider.logger.info(f'Bulk insert {len(data_li)} items successfully')
        self.data_li.clear()

    def process_item(self, item, spider):
        data = ItemAdapter(item).asdict()
        self.data_li.append(data)
        if len(self.data_li) >= self.bulk_insert:
            self.insert_data(spider, self.data_li)
        return item
