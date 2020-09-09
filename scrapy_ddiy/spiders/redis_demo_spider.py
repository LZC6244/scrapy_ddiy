# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy_ddiy.utils.spiders.ddiy_redis import DdiyRedisSpider

"""
scrapy_ddiy 示例爬虫
"""


class DemoSpider(DdiyRedisSpider):
    name = 'redis_demo_spider'
    description = 'scrapy_ddiy - 示例爬虫'
    start_urls = ['https://www.baidu.com/']
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 1,
    }

    def make_request_from_data(self, data):
        demo_url = f'https://www.baidu.com/#{data}'
        yield Request(url=demo_url, callback=self.parse, dont_filter=True)

        demo_url_2 = f'https://www.baidu.com/#{data}-{data}'
        yield Request(url=demo_url_2, callback=self.parse, dont_filter=True)

    def parse(self, response):
        self.logger.info(f"{response.url} ==> I'm a redis demo spider.")
