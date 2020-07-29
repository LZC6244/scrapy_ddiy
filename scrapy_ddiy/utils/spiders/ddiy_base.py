# -*- coding: utf-8 -*-
import os
import redis
import scrapy
import pymongo
from datetime import datetime
from scrapy.item import Item, Field
from scrapy_ddiy.utils.common import get_request_md5

"""
scrapy_ddiy 基本爬虫
"""


class DdiyBaseSpider(scrapy.Spider):
    name = 'ddiy_base'

    # 管道配置
    # 数据库表名
    table_name_ddiy = None
    # 数据库表名 for MongoDB
    table_name_mongo = None

    start_urls = ['https://www.baidu.com/']

    # custom_settings 优先级高于 ddiy_settings
    ddiy_settings = {
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 1,
    }
    # 预设给爬虫使用的 Redis 连接（如 scrapy_redis 、 记录某些特定数据）
    redis_cli: redis.Redis
    # 预设给爬虫使用的 MongoDB 连接（如记录爬虫异常信息）
    mongo_cli: pymongo.MongoClient

    @classmethod
    def update_settings(cls, settings):
        now = datetime.now().strftime('%Y-%m-%dT%H_%M_%S')
        if settings.getbool('MAKE_LOG_FILE'):
            log_file = settings.get('LOG_FILE') or f'spider_logs/{cls.name}/{cls.name}__{now}__{os.getpid()}.log'
            make_log_dir(log_file)
            settings.setdict({'LOG_FILE': log_file}, priority='spider')
        settings.setdict(cls.ddiy_settings or {}, priority='spider')
        settings.setdict(cls.custom_settings or {}, priority='spider')

    def custom_init(self, *args, **kwargs):
        pass

    def base_init(self, *args, **kwargs):
        if hasattr(self, 'server'):
            self.redis_cli = self.server
        else:
            self.redis_cli = redis.Redis(host=self.settings.get('REDIS_HOST'), port=self.settings.get('REDIS_PORT'),
                                         **self.settings.getdict('REDIS_PARAMS'))
        self.mongo_cli = pymongo.MongoClient(self.settings.get('MONGO_URI'), **self.settings.getdict('MONGO_PARAMS'))
        self.mongo_cli = pymongo.MongoClient(self.settings.get('MONGO_URI'), **self.settings.getdict('MONGO_PARAMS'))

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        spider.base_init(*args, **kwargs)
        spider.custom_init(*args, **kwargs)
        return spider

    @staticmethod
    def _adjust_item(parsed_item: dict):
        item = Item()
        for k, v in parsed_item.items():
            item.fields[k] = Field()
            item[k] = v
        return item

    def process_parsed_item(self, response, parsed_item: dict, set_id=True):
        if set_id:
            # 默认不覆盖 parsed_item 中带过来的 _id
            parsed_item.setdefault('_id', get_request_md5(response.request))
        parsed_item['crawl_time'] = datetime.now()
        return self._adjust_item(parsed_item)


def make_log_dir(log_file: str = None):
    if not log_file:
        return
    current_dir = os.path.dirname(__file__)
    log_dir = os.path.join(current_dir, '../../..', os.path.split(log_file)[0])
    os.makedirs(log_dir, exist_ok=True)
    # print(os.path.normpath(log_dir))
