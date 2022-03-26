# -*- coding: utf-8 -*
"""
1. 记录开始发起请求和解析响应（可选）
2. 为请求设置默认 errback
3. 将 'start_time' 和 'finish_time '从 utc 时间设置为北京时间
"""
import scrapy
from scrapy import signals
from types import MethodType
from datetime import timedelta, datetime
from twisted.internet import task
from twisted.python.failure import Failure


def default_err_back(spider: scrapy.Spider, failure: Failure):
    err_msg = repr(failure.value)
    request = getattr(failure, 'request')
    err_back = spider.logger.error if hasattr(spider, 'logger') else print
    err_back(f'{err_msg}\nRaw request: [{request.method}] {request.url}  {request.body[:50]}')


class LogCrawlMiddleware(object):
    log_crawling: bool
    log_parsing: bool
    mark_start = True
    stats_to_db_task: task.LoopingCall

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.close_spider, signal=signals.spider_closed)
        return s

    def spider_opened(self, spider):
        spider.crawler.stats.get_stats()['start_time'] += timedelta(hours=8)
        self.log_crawling = spider.settings.getbool('LOG_CRAWLING')
        self.log_parsing = spider.settings.getbool('LOG_PARSING')
        spider.ddiy_default_err_back = MethodType(default_err_back, spider)
        if spider.is_online:
            spider.logger.info('Using the online environment! Be careful!!')
            # 每隔1小时上报一次爬虫状态
            self.stats_to_db_task = task.LoopingCall(self.crawl_stats_to_db, spider=spider)
            self.stats_to_db_task.start(3600)

    def process_request(self, request, spider):
        if not request.errback:
            # 此处必须传方法，不能传函数（譬如利用匿名函数使用 default_err_back 函数）
            # scrapy 爬虫可传函数， scrapy_redis 爬虫仅能传方法
            setattr(request, 'errback', spider.ddiy_default_err_back)
        if self.log_crawling:
            spider.logger.info(f'Crawling ==> [{request.method}] {request.url}  {request.body[:50]}')
        return None

    def process_response(self, request, response, spider):
        if response.status != 200:
            spider.logger.warning(
                f'Got non-200 response ==> [{response.status}-{request.method}] {request.url}  {request.body[:50]}')
        if self.log_parsing:
            spider.logger.info(f'Parsing ==> [{request.method}] {request.url}  {request.body[:50]}')
        return response

    def close_spider(self, spider):
        spider_stats = spider.crawler.stats.get_stats()
        spider_stats['finish_time'] += timedelta(hours=8)
        start_time = spider_stats['start_time']
        finish_time = spider_stats['finish_time']
        spider_stats['elapsed_time_readable'] = str(finish_time - start_time)[:-1]

        if spider.is_online:
            if self.stats_to_db_task.running:
                self.stats_to_db_task.stop()
            self.crawl_stats_to_db(spider, 'finished')
        spider.mongo_cli.close()

    def crawl_stats_to_db(self, spider, status='crawling'):
        """
        将爬虫状态保存至 MongoDB
        :param spider:
        :param status: 爬取状态
        :return:
        """
        time_fmt = '%Y-%m-%d %H:%M:%S'
        stats_info = spider.crawler.stats.get_stats()
        start_time = stats_info['start_time'].strftime(time_fmt)
        record_time = datetime.now().strftime(time_fmt)
        finish_time = stats_info.get('finish_time')
        if finish_time:
            finish_time = finish_time.strftime(time_fmt)
        finish_reason = stats_info.get('finish_reason', None)
        item_scraped_count = stats_info.get('item_scraped_count', 0)
        # redis 爬虫，已获取种子数
        fetch_seed_count = stats_info.get('fetch_seed_count', 0)
        # 解析异常数
        parse_error_count = stats_info.get('parse_error_count', 0)
        # 超出最大重试次数
        max_retry_count = stats_info.get('retry/max_reached', 0)
        # 保存数据失败次数
        save_item_error_count = stats_info.get('save_item_error_count', 0)
        if self.mark_start:
            status = 'start'
            self.mark_start = False
        info = {
            'spider_name': spider.name,
            'server_ip': spider.local_ip,
            'pid': spider.pid,
            'start_time': start_time,
            'record_time': record_time,
            'status': status,
            'finish_time': finish_time,
            'finish_reason': finish_reason,
            'item_scraped_count': item_scraped_count,
            'fetch_seed_count': fetch_seed_count,
            'parse_error_count': parse_error_count,
            'max_retry_count': max_retry_count,
            'save_item_error_count': save_item_error_count,
        }
        spider.mongo_coll_stats.insert_one(info)
        spider.logger.info('The spider status has been put into the mongodb')
