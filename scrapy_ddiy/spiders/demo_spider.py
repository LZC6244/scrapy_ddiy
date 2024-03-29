# -*- coding: utf-8 -*-

from scrapy_ddiy import DdiyBaseSpider

"""
scrapy_ddiy 示例爬虫
"""


class DemoSpider(DdiyBaseSpider):
    name = 'demo_spider'
    description = 'scrapy_ddiy - 基础示例爬虫'
    start_urls = ['https://www.baidu.com/'] * 5
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 1,
        'ITEM_PIPELINES': {
            'scrapy_ddiy.pipelines.mongodb.MongodbPipeline': 300,
        }
    }

    def parse(self, response, **kwargs):
        self.logger.info("I'm a demo spider.")
        item = {'k1': 'v1', 'k2': 'v2'}
        item = self.process_parsed_item(response, item)
        yield item
