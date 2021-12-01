# -*- coding: utf-8 -*-
import os
import requests
from time import sleep
from scrapy import signals
from twisted.internet import defer
from twisted.internet.error import (
    ConnectError,
    ConnectionDone,
    ConnectionLost,
    ConnectionRefusedError,
    DNSLookupError,
    TCPTimedOutError,
    TimeoutError,
)
from scrapy.exceptions import IgnoreRequest
from twisted.web.client import ResponseFailed
from scrapy.core.downloader.handlers.http11 import TunnelError


class GlidedSkyMiddleware(object):
    cookies: dict
    proxy_server_url: str
    interval_get_proxy: int
    EXCEPTIONS_TO_RETRY = (defer.TimeoutError, TimeoutError, DNSLookupError,
                           ConnectionRefusedError, ConnectionDone, ConnectError,
                           ConnectionLost, TCPTimedOutError, ResponseFailed,
                           IOError, TunnelError)

    def __init__(self):
        self.glided_sky_cookie_set_name = 'glided_sky_cookie'
        self.glided_sky_enable_proxy = False

        # GlidedSky ip反爬题目1、2专用
        self.used_proxy_set = set()
        self.proxies_li = []
        self.retry_http_codes = {500, 502, 503, 504, 522, 524, 408, 429, 403}

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        settings = crawler.settings
        if settings.getbool('GLIDED_SKY_ENABLE_PROXY'):
            proxy_server_url = settings.get('PROXY_SERVER_URL') or os.environ.get('PROXY_SERVER_URL')
            if not proxy_server_url:
                raise AttributeError('Please set the [ PROXY_SERVER_URL ] for the spider')
            setattr(s, 'proxy_server_url', proxy_server_url)
            setattr(s, 'glided_sky_enable_proxy', True)
            setattr(s, 'interval_get_proxy', settings.get('INTERVAL_GET_PROXY', 15))
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def get_proxy(self):
        r = requests.get(self.proxy_server_url)
        return r.text.split()

    def set_proxy(self, request, spider):
        while not self.proxies_li:
            proxies_li = self.get_proxy()
            spider.logger.info('获取一批未检查代理完成 ...')
            for p in proxies_li:
                ip = p.split(':')[0]
                if ip not in self.used_proxy_set:
                    self.proxies_li.append(p)
            if not self.proxies_li:
                spider.logger.info(f'暂时获取不到未被封禁的 IP ，等待 {self.interval_get_proxy} 秒重新获取')
                sleep(self.interval_get_proxy)
        proxy = self.proxies_li.pop()
        proxy_ip = proxy.split(':')[0]
        scheme = request.url.split('://')[0]
        request.meta['proxy'] = f'{scheme}://{proxy}'
        spider.logger.info(f'Use proxy => {proxy_ip}')
        self.used_proxy_set.add(proxy_ip)

    def spider_opened(self, spider):
        glidedsky_session = spider.redis_cli.get(self.glided_sky_cookie_set_name)
        if not glidedsky_session:
            raise ValueError(f'[ {self.glided_sky_cookie_set_name} ] not exists')
        self.cookies = {'glidedsky_session': glidedsky_session.decode()}

    def process_request(self, request, spider):
        request.cookies = self.cookies
        if self.glided_sky_enable_proxy and request.meta.get('set_proxy'):
            self.set_proxy(request, spider)

    def process_response(self, request, response, spider):
        """
        判断 cookie 是否失效
        因为用到了 response.body  （解析response内容）
        故此中间件序号需小于590
        scrapy 默认配置           （'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,）
        process_request   顺序执行
        process_response  逆序执行
        """
        if '/login' in response.url or '/login' in response.xpath('//title/text()').get(''):
            spider.crawler.engine.close_spider(spider, 'cookie_invalid')
            raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        if self.glided_sky_enable_proxy and request.meta.get('set_proxy') and \
                isinstance(exception, self.EXCEPTIONS_TO_RETRY):
            # 忽略全部异常，进行重试（题目：IP反爬）
            self.set_proxy(request, spider)
            request.dont_filter = True
            return request
