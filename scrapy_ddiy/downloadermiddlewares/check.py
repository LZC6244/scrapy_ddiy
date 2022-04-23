# -*- coding: utf-8 -*-

from scrapy import signals
from scrapy.exceptions import UsageError
from twisted.web._responses import RESPONSES

"""
中间件功能：检查响应，决定是否重试
实现方式：在请求中传入指定参数（check_dict），检查后如需重试则传入自定义响应状态码
        PS：默认配置中已加入重试状态码
        
        check_dict = {
        'empty_response':True,
        'xpath':['//div[@xx=xx]',...],
        'not_xpath':['//div[@xx=xx]',...],
        TODO: 'headers_contain'
        }
"""


class CheckMiddleware(object):
    custom_retry_http_code: int

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def spider_opened(self, spider):
        settings = spider.settings
        self.custom_retry_http_code = settings.getint('CUSTOM_RETRY_HTTP_CODE')
        # 自定义重试时的说明字符串
        RESPONSES[self.custom_retry_http_code] = b'Custom Retry'

    def process_response(self, request, response, spider):
        check_dict = request.meta.get('check_dict')
        if not check_dict:
            return response
        if 'empty_response' in check_dict:
            # TODO: 具体怎么检查空响应？
            response.status = self.custom_retry_http_code
            spider.logger.info('[check] retry by "empty_response"')
        elif 'xpath' in check_dict:
            assert isinstance(check_dict['xpath'], list), '"xpath" must be a list'
            for x in check_dict['xpath']:
                if response.xpath(x):
                    response.status = self.custom_retry_http_code
                    spider.logger.info('[check] retry by "xpath"')
                    break
        elif 'not_xpath' in check_dict:
            assert isinstance(check_dict['not_xpath'], list), '"not_xpath" must be a list'
            for x in check_dict['not_xpath']:
                if not response.xpath(x):
                    response.status = self.custom_retry_http_code
                    spider.logger.info('[check] retry by "not_xpath"')
                    break
        else:
            raise UsageError
        return response
