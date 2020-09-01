# -*- coding: utf-8 -*
"""
1. 记录开始发起请求和解析响应（可选）
2. 为请求设置默认 errback
3. 将 'start_time' 和 'finish_time '从 utc 时间设置为北京时间
"""
import scrapy
from scrapy import signals
from twisted.python.failure import Failure
from datetime import timedelta


def default_err_back(spider: scrapy.Spider, failure: Failure):
    err_msg = repr(failure.value)
    request = getattr(failure, 'request')
    err_back = spider.logger.error if hasattr(spider, 'logger') else print
    err_back(f'{err_msg}\nRaw request: [{request.method}] {request.url}  {request.body[:50]}')


class LogCrawl(object):
    log_crawling: bool
    log_parsing: bool

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def spider_opened(self, spider):
        spider.crawler.stats.get_stats()['start_time'] += timedelta(hours=8)
        self.log_crawling = spider.settings.getbool('LOG_CRAWLING')
        self.log_parsing = spider.settings.getbool('LOG_PARSING')

    def process_request(self, request, spider):
        if not request.errback:
            setattr(request, 'errback', lambda failure: default_err_back(spider, failure))
        if self.log_crawling:
            spider.logger.info(f'Crawling ==> [{request.method}] {request.url}  {request.body[:50]}')
        return None

    def process_response(self, request, response, spider):
        if response.status != 200:
            spider.logger.warning(
                f'Got not 200 response ==> [{request.method}] {request.url}  {request.body[:50]}')
        if self.log_parsing:
            spider.logger.info(f'Parsing ==> [{request.method}] {request.url}  {request.body[:50]}')
        return response

    def close_spider(self, spider):
        spider.crawler.stats.get_stats()['finish_time'] += timedelta(hours=8)
