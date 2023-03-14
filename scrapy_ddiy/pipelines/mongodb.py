# -*- coding: utf-8 -*-
"""
MongoDB Pipeline
"""
import pymongo
from datetime import datetime
from twisted.internet import task
from itemadapter import ItemAdapter
from pymongo.errors import BulkWriteError, DuplicateKeyError


class MongodbPipeline(object):
    exception_info: dict = None
    mongo_coll: pymongo.collection.Collection
    check_exception_task: task.LoopingCall
    time_fmt = '%Y-%m-%d %H:%M:%S'

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
        if spider.is_online:
            self.check_exception_task = task.LoopingCall(self.send_msg, spider=spider)
            self.check_exception_task.start(interval=1800)
        else:
            # 防止开发爬虫时污染线上数据
            self.mongo_db = 'scrapy_ddiy_test'
            spider.logger.info(f'Non-online environment! Set the mongodb database table name to "{self.mongo_db}"')

        mongo_coll = getattr(spider, 'table_name_ddiy', None) or spider.name
        spider.logger.info(f'[{self.__class__.__name__}] use database => {self.mongo_db}.{mongo_coll}')
        self.mongo_coll = self.mongo_cli[self.mongo_db][mongo_coll]
        # 为 MongoDB 集合创建索引
        # 目前仅支持单字段索引，若要创建复合索引或进行其他复杂操作，请自行在 spider.custom_init 方法中执行
        for index_name, index_sort in self.mongo_index_dict.items():
            create_index = self.mongo_coll.create_index([(index_name, index_sort)])
            spider.logger.info(f'Created index => {create_index}')

    def close_spider(self, spider):
        if self.data_li:
            self.insert_data(spider, self.data_li)
        self.mongo_cli.close()
        if spider.is_online:
            if self.check_exception_task.running:
                self.check_exception_task.stop()
        self.send_msg(spider=spider, cron=False)

    def insert_data(self, spider, data_li: list):
        try:
            self.mongo_coll.insert_many(data_li, ordered=False)
        except BulkWriteError as e:
            # 插入重复数据（_id）时会报此错误
            pass
        except Exception as e:
            warn_time = datetime.now().strftime(self.time_fmt)
            start_time = spider.crawler.stats.get_value('start_time').strftime(self.time_fmt)
            for _data in self.data_li:
                try:
                    self.mongo_coll.insert_one(_data)
                except DuplicateKeyError:
                    pass
                except Exception as e2:
                    spider.logger.error(f'Invalid data to MongoDB:\n{_data}')
                    spider.crawler.stats.inc_value('save_item_error_count')
                    save_item_error_count = spider.crawler.stats.get_value('save_item_error_count')

                    exception_info = {'spider_name': spider.name, 'start_time': start_time,
                                      'server_ip': spider.local_ip, 'pid': spider.pid, 'exec_info': repr(e2),
                                      'warn_reason': 'save_item_error', 'save_item_error_count': save_item_error_count,
                                      'warn_time': warn_time}
                    self.exception_info = exception_info
                    if save_item_error_count == 1:
                        self.send_msg(spider=spider, cron=False)

        spider.logger.info(f'Bulk insert {len(data_li)} items successfully')
        self.data_li.clear()

    def process_item(self, item, spider):
        data = ItemAdapter(item).asdict()
        self.data_li.append(data)
        if len(self.data_li) >= self.bulk_insert:
            self.insert_data(spider, self.data_li)
        return item

    def send_msg(self, spider, cron: bool = True):
        now = datetime.now()
        if not self.exception_info:
            return
        if cron and (now.hour < 8 or now.hour >= 21):
            return
        mail_subject = f'Spider-Warning: [save_item_error] {spider.name}'
        spider.send_mail(mail_subject=mail_subject, warn_msg=self.exception_info)
        self.exception_info = dict()
