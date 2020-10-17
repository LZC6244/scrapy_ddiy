# -*- coding: utf-8 -*-
import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


class GlidedSkyMiddleware(UserAgentMiddleware):

    def process_response(self, request, response, spider):
        """判断 cookie 是否失效"""
        if '/login' in response.url:
            spider.crawler.engine.close_spider(spider, 'cookie invalid')
        return response
