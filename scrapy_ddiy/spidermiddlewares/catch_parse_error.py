# -*- coding: utf-8 -*-
import pickle
import traceback
from scrapy import signals
from datetime import datetime
from twisted.internet import task
from scrapy.utils.reqser import request_to_dict

"""
捕获爬虫解析异常中间件
"""


class CatchParseErrorMiddleware(object):
    close_spider_when_parsed_error: bool
    start_time: str
    check_exception_task: task.LoopingCall
    exception_info: dict = None
    time_fmt = '%Y-%m-%d %H:%M:%S'

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_exception(self, response, exception, spider):
        spider.crawler.stats.inc_value('parse_error_count')
        spider.crawler.stats.inc_value(f'parse_error_count/response_status_{response.status}')

        warn_time = datetime.now()
        callback_name = getattr(response.request.callback, '__name__', 'parse')
        request = pickle.dumps(request_to_dict(response.request, spider))
        exec_info = traceback.format_exc()

        exception_info = {'spider_name': spider.name, 'start_time': self.start_time, 'server_ip': spider.local_ip,
                          'pid': spider.pid, 'warn_reason': 'parse_error', 'callback_name': callback_name,
                          'request': request, 'response': response.body, 'exec_info': exec_info,
                          'warn_time': warn_time.strftime(self.time_fmt)}
        spider.mongo_coll_exception.insert_one(exception_info)

        headers_info = response.request.headers.to_string().decode()
        request_info = f'<[{response.status}-{response.request.method}] {response.request.url}  ' \
                       f'{response.request.body}n>\n\nRequest Headers ↓↓↓\n{headers_info}'
        exception_info.pop('response')
        exception_info.pop('request')
        exception_info['request_info'] = request_info
        parse_error_count = spider.crawler.stats.get_value('parse_error_count')
        exception_info['parse_error_count'] = parse_error_count
        self.exception_info = exception_info
        # if parse_error_count == 1 and spider.is_online:
        #     self.send_msg(spider=spider, cron=False)

        if self.close_spider_when_parsed_error:
            spider.crawler.engine.close_spider(spider, 'close_spider_when_parsed_error')

    def spider_opened(self, spider):
        self.start_time = spider.crawler.stats.get_value('start_time').strftime(self.time_fmt)

        self.close_spider_when_parsed_error = spider.settings.getbool('CLOSE_SPIDER_WHEN_PARSED_ERROR')
        # if spider.is_online:
        #     self.check_exception_task = task.LoopingCall(self.send_msg, spider=spider)
        #     self.check_exception_task.start(interval=1800)

    def close_spider(self, spider):
        if spider.is_online:
            if self.check_exception_task.running:
                self.check_exception_task.stop()
            # self.send_msg(spider=spider, cron=False)

    def send_msg(self, spider, cron: bool = True):
        now = datetime.now()
        if not self.exception_info:
            return
        if cron and (now.hour < 8 or now.hour >= 21):
            return
        mail_subject = f'Spider-Warning: [parse_error] {spider.name}'
        # spider.send_mail(mail_subject=mail_subject, warn_msg=self.exception_info)
        self.exception_info = dict()
