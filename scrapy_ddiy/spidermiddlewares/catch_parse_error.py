# -*- coding: utf-8 -*-
import os
import traceback
from copy import deepcopy
from scrapy import signals
from datetime import datetime
from pymongo.errors import DuplicateKeyError
from scrapy_ddiy.utils.common import get_str_md5

"""
捕获爬虫解析异常中间件
"""


class CatchParseErrorMiddleware(object):
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
        callback_name = getattr(response.request.callback, '__name__', 'parse')
        headers_info = response.request.headers.to_string().decode()
        request_info = f'<[{response.status}-{response.request.method}] {response.request.url}  ' \
                       f'{response.request.body}>\n\nRequest Headers ↓↓↓\n{headers_info}'
        exec_info = traceback.format_exc()

        # 使用 '服务器ip+进程号+爬虫启动时间+异常详情' 计算异常MD5
        exception_md5 = get_str_md5(f'{spider._local_ip}{self.pid}{self.start_time}{exec_info}')
        exception_info = {'_id': exception_md5, 'server_ip': spider._local_ip,
                          'pid': self.pid, 'callback_name': callback_name, 'exec_info': exec_info,
                          'request_info': request_info, 'warn_time': datetime.now()}
        if spider.is_online:
            exception_info_mongo = deepcopy(exception_info)
            spider.send_mail('Parse Error', exception_info)
            exception_info_mongo['response_info'] = response.text
            try:
                spider.mongo_coll_exec.insert_one(exception_info_mongo)
                spider.logger.warning(f'Parsed error id is {exception_md5}')
            except DuplicateKeyError:
                # 不插入重复异常
                pass
            except Exception as e:
                spider.send_ding_bot_msg(repr(e))
        spider.crawler.stats.inc_value('parse_error_count')
        spider.crawler.stats.inc_value(f'parse_error_count/response_status_{response.status}')
        if not spider.is_online and self.close_spider_when_parsed_error:
            spider.crawler.engine.close_spider(spider, 'Parsed error when spider running in not online environment')

    def spider_opened(self, spider):
        self.start_time = str(spider.crawler.stats.get_value('start_time'))
        self.pid = str(os.getpid())
        self.close_spider_when_parsed_error = spider.settings.getbool('CLOSE_SPIDER_WHEN_PARSED_ERROR')
