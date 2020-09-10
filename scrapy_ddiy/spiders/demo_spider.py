# -*- coding: utf-8 -*-

from scrapy_ddiy.utils.spiders.ddiy_base import DdiyBaseSpider

"""
scrapy_ddiy 示例爬虫
"""


class DemoSpider(DdiyBaseSpider):
    name = 'demo_spider'
    description = 'scrapy_ddiy - Redis示例爬虫'
    start_urls = ['https://www.baidu.com/']
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 1,
    }

    def parse(self, response):
        self.logger.info("I'm a demo spider.")
        item = {'k1': 'v1', 'k2': 'v2'}
        item = self.process_parsed_item(response, item)
        yield item
