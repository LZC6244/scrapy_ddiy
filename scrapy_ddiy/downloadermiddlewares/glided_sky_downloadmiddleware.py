# -*- coding: utf-8 -*-
from scrapy import signals


class GlidedSkyMiddleware(object):
    cookies: dict

    def __init__(self):
        self.glided_sky_cookie_set_name = 'glided_sky_cookie'

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def spider_opened(self, spider):
        glidedsky_session = spider.redis_cli.get(self.glided_sky_cookie_set_name)
        if not glidedsky_session:
            raise ValueError(f'[ {self.glided_sky_cookie_set_name} ] not exists')
        self.cookies = {'glidedsky_session': glidedsky_session.decode()}

    def process_request(self, request, spider):
        request.cookies = self.cookies

    def process_response(self, request, response, spider):
        """判断 cookie 是否失效"""
        if '/login' in response.url:
            spider.crawler.engine.close_spider(spider, 'cookie invalid')
        return response
