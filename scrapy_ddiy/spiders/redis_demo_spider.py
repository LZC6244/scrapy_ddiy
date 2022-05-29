# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy_ddiy import DdiyRedisSpider

"""
scrapy_ddiy 示例爬虫
"""


class RedisDemoSpider(DdiyRedisSpider):
    name = 'redis_demo_spider'
    description = 'scrapy_ddiy -  Redis示例爬虫'
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 1,
        'ITEM_PIPELINES': {
            'scrapy_ddiy.pipelines.mongodb.MongodbPipeline': 300,
        },
        'SCHEDULER': 'scrapy_redis.scheduler.Scheduler',
        'DUPEFILTER_CLASS': 'scrapy_redis.dupefilter.RFPDupeFilter',

        # 'SCHEDULER': 'scrapy_ddiy.utils.scheduler.SchedulerDdiy',
        # 'DUPEFILTER_CLASS': 'scrapy_ddiy.utils.dupefilter.RedisBloomDupeFilter',
        # 'REDIS_BLOOM_CAPACITY': 1000,
        # 'REDIS_BLOOM_ERROR_RATE': 0.01,
    }

    def make_request_from_data(self, data):
        demo_url = f'https://www.baidu.com/s?wd={data}'
        yield Request(url=demo_url, callback=self.parse, meta={'dont_redirect': True})

        demo_url_2 = f'https://www.baidu.com/s?wd={data}test{data}'
        yield Request(url=demo_url_2, callback=self.parse, meta={'dont_redirect': True})

    def parse(self, response, **kwargs):
        self.logger.info(f"{response.url} ==> I'm a redis demo spider.")
        item = {'k1': 'v1', 'k2': 'v2'}
        item = self.process_parsed_item(response, item)
        yield item
