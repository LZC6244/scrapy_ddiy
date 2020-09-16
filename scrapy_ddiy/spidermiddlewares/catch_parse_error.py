# -*- coding: utf-8 -*-
import os
import traceback
from scrapy import signals
from datetime import datetime
from pymongo.errors import DuplicateKeyError
from scrapy_ddiy.utils.common import get_str_md5

"""
捕获爬虫解析异常中间件
"""


class CatchParseErrorMiddleware(object):
    save_exception_to_mongodb = False
    close_spider_when_parsed_error: bool
    start_time: str
    pid: str

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        callback_name = getattr(response.request.callback, '__name__', 'parse')
        headers_info = response.request.headers.to_string().decode()
        request_info = f'<[{response.status}-{response.request.method}] {response.request.url}  ' \
                       f'{response.request.body}>\n\nRequest Headers ↓↓↓\n{headers_info}'
        exec_info = traceback.format_exc()

        # 使用 '服务器ip+进程号+爬虫启动时间+异常详情' 计算异常MD5
        exception_md5 = get_str_md5(f'{spider._local_ip}{self.pid}{self.start_time}{exec_info}')
        exception_info = {'_id': exception_md5, 'exception_type': 'Parse Error', 'server_ip': spider._local_ip,
                          'pid': self.pid, 'callback_name': callback_name, 'exec_info': exec_info,
                          'request_info': request_info, 'response_info': response.text, 'warn_time': datetime.now()}
        if hasattr(spider, 'mongo_coll'):
            try:
                # spider.mongo_coll.insert_one(exception_info)
                spider.logger.warning(f'Parsed error id is {exception_md5}')
            except DuplicateKeyError:
                # 不插入重复异常
                pass
            except Exception as e:
                spider.send_ding_bot_msg(repr(e))
        if getattr(spider, '_exceptions_mail_on', False):
            spider._exceptions_li.append(exception_info)
        spider.crawler.stats.inc_value('parse_error_count')
        # spider.crawler.stats.inc_value(f'parse_error_count/response_status_{response.status}')
        # spider.logger.error(msg)
        # if not spider.is_online and self.close_spider_when_parsed_error:
        #     spider.crawler.engine.close_spider(spider, 'Parsed error when spider running in not online environment')

    def spider_opened(self, spider):
        self.start_time = str(spider.crawler.stats.get_value('start_time'))
        self.pid = str(os.getpid())
        if spider.is_online:
            self.save_exception_to_mongodb = True
        self.close_spider_when_parsed_error = spider.settings.getbool('CLOSE_SPIDER_WHEN_PARSED_ERROR')


class TEST(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        spider.logger.info('hhhhhhhhhhhhhh')

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
