# -*- coding: utf-8 -*-
import os
import json
import redis
import pymongo
from scrapy import Spider
from datetime import datetime
from scrapy.item import Item, Field
from scrapy_ddiy.utils.common import get_request_md5, get_local_ip

"""
scrapy_ddiy 基础爬虫
"""


class DdiyBaseSpider(Spider):
    name = 'ddiy_base'
    # 爬虫描述，必填
    description: str = None

    # 管道配置
    # 数据库表名
    table_name_ddiy = None

    # custom_settings 优先级高于 _ddiy_settings
    _ddiy_settings = {}
    # 预设给爬虫使用的 Redis 连接（如 scrapy_redis 、 记录告警信息）
    redis_cli: redis.Redis
    # 预设给爬虫使用的 MongoDB 连接（如记录爬虫异常信息）
    mongo_cli: pymongo.MongoClient
    # 本机内网 IP
    _local_ip: str

    @classmethod
    def update_settings(cls, settings):
        now = datetime.now().strftime('%Y-%m-%dT%H_%M_%S')
        settings.setdict(cls._ddiy_settings or {}, priority='spider')
        settings.setdict(cls.custom_settings or {}, priority='spider')
        if settings.getbool('MAKE_LOG_FILE'):
            log_file = settings.get('LOG_FILE', f'spider_logs/{cls.name}/{cls.name}__{now}__{os.getpid()}.log')
            make_log_dir(log_file)
            settings.setdict({'LOG_FILE': log_file}, priority='spider')

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
        self._local_ip = get_local_ip()
        if os.environ.get('ENV_FLAG_DDIY') != 'online':
            # 防止开发爬虫时污染线上数据
            self.logger.info('Non-online environment!Set the database table name to "scrapy_ddiy_test"')
            self.table_name_ddiy = 'scrapy_ddiy_test'

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        spider.base_init(*args, **kwargs)
        spider.custom_init(*args, **kwargs)
        assert spider.mongo_cli.server_info(), 'MongoDB failed to establish a connection, please check the settings'
        assert spider.redis_cli.info(), 'Redis failed to establish a connection, please check the settings'
        assert spider.description, 'Please fill in a description for the Spider, such as: "Sample Spider", ' \
                                   '"XX-Spider" ... '

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

    def send_ding_bot_msg(self, warn_msg: str):
        time_format = '%Y-%m-%d %H:%M:%S'
        start_time = self.crawler.stats.get_stats()['start_time'].strftime(time_format)
        warn_time = datetime.now().strftime(time_format)
        msg_dict = {'start_time': start_time, 'warn_time': warn_time,
                    'spider_name': f'[{self.name}] {self.description}', 'warn_msg': warn_msg,
                    'server_ip': self._local_ip, 'pid': os.getpid()}
        self.crawler.stats.inc_value('warn_msg_count/ding_bot')
        self.redis_cli.rpush(self.settings.get('WARN_MESSAGES_LIST'), json.dumps(msg_dict, ensure_ascii=False))

    def closed(self, reason):
        self.mongo_cli.close()
        self.redis_cli.close()


def make_log_dir(log_file: str = None):
    if not log_file:
        return
    current_dir = os.path.dirname(__file__)
    log_dir = os.path.join(current_dir, '../../..', os.path.split(log_file)[0])
    os.makedirs(log_dir, exist_ok=True)
    # print(os.path.normpath(log_dir))
