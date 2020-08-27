# -*- coding: utf-8 -*-

from scrapy_ddiy.utils.spiders.ddiy_base import DdiyBaseSpider

"""
scrapy_ddiy 示例爬虫
"""


class DemoSpider(DdiyBaseSpider):
    name = 'demo_spider'
    description = 'scrapy_ddiy - 示例爬虫'

    def parse(self, response):
        self.logger.info("I'm a demo spider.")
