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
        exec_info = traceback.format_exc() if spider.send_msg_method != 'dingding' else None

        if spider.save_and_send_exception:
            # 使用 '服务器ip+进程号+爬虫启动时间+异常详情' 计算异常 MD5
            exception_md5 = get_str_md5(f'{spider._local_ip}{self.pid}{self.start_time}{exec_info}')
            spider.crawler.stats.inc_value(f'parse_error_count/_id/{exception_md5}')
            exception_info = {'_id': exception_md5, 'server_ip': spider._local_ip, 'pid': self.pid,
                              'callback_name': callback_name, 'request_info': request_info,
                              'warn_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'response': response.text}
            try:
                spider.mongo_coll_exec.insert_one(exception_info)
                exception_info.pop('response')
                exception_info['exception_id'] = exception_info.pop('_id')
                # 重复异常不发送提醒消息
                spider.send_msg(method=spider.send_msg_method, warn_msg=exec_info, warn_type='Parse Error',
                                **exception_info)
            except DuplicateKeyError:
                # 不插入重复异常
                pass
        spider.crawler.stats.inc_value('parse_error_count')
        spider.crawler.stats.inc_value(f'parse_error_count/response_status_{response.status}')
        if self.close_spider_when_parsed_error:
            spider.crawler.engine.close_spider(spider, 'Parsed error when spider running in not online environment')

    def spider_opened(self, spider):
        self.start_time = str(spider.crawler.stats.get_value('start_time'))
        self.pid = str(os.getpid())
        self.close_spider_when_parsed_error = spider.settings.getbool('CLOSE_SPIDER_WHEN_PARSED_ERROR')
