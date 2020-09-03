# -*- coding: utf-8 -*-
from copy import deepcopy
from inspect import isgenerator
from scrapy_redis import defaults
from scrapy_redis.spiders import RedisSpider
from scrapy.exceptions import DontCloseSpider
from scrapy_ddiy.utils.spiders.ddiy_base import DdiyBaseSpider

"""
scrapy_ddiy redis爬虫
"""


class DdiyRedisSpider(DdiyBaseSpider, RedisSpider):
    name = 'ddiy_redis'
    # 从 redis 队列获取不到种子的统计次数，获取不到种子时 scrapy 会调用 spider_idle 方法
    _idle_times = 0
    # 允许从 redis 队列获取不到种子的最大次数，统计次数达到/超过该值时结束爬虫
    _idle_times_max: int
    _ddiy_settings = deepcopy(DdiyBaseSpider._ddiy_settings)
    _ddiy_settings.update({
        'SCHEDULER': 'scrapy_redis.scheduler.Scheduler',
        'DUPEFILTER_CLASS': 'scrapy_redis.dupefilter.RFPDupeFilter',
    })

    def base_init(self, *args, **kwargs):
        super().base_init(*args, **kwargs)
        self._idle_times_max = self.settings.getint('IDLE_TIMES_MAX', 3)

    def spider_idle(self):
        """重写 RedisSpider spider_idle 方法，解决空跑（无限等待种子）"""
        self.schedule_next_requests()
        if self._idle_times >= self._idle_times_max:
            self.closed(reason=f'Close spider after not got seed from redis queue{self._idle_times_max} times.')
        else:
            raise DontCloseSpider

    def next_requests(self):
        """重写 RedisSpider next_requests 方法"""
        use_set = self.settings.getbool('REDIS_START_URLS_AS_SET', defaults.START_URLS_AS_SET)
        fetch_one = self.server.spop if use_set else self.server.lpop
        found = 0
        while found < self.redis_batch_size:
            data = fetch_one(self.redis_key)
            if not data:
                # Queue empty.
                break
            try:
                req = self.make_request_from_data(data)
                # When 'make_request_from_data' method use like 'yield Request'
                if isgenerator(req):
                    req = next(req)
            except Exception as e:
                self.logger.exception(f'Parsed seed error\nseed raw: {data}')
                self.crawler.stats.inc_value('parsed_seed_error')
                continue
            if req:
                yield req
                found += 1
            else:
                self.logger.debug("Request not made from data: %r", data)
        if found == 0:
            self._idle_times += 1
            self.logger.info('Wow, got a empty redis queue ~ ~ ~')
        else:
            self._idle_times = 0
            self.logger.debug("Read %s requests from '%s'", found, self.redis_key)
