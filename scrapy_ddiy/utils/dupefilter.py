# -*- coding: utf-8 -*-
import redis
from redisbloom.client import Client
from scrapy_redis.dupefilter import RFPDupeFilter


class RedisBloomDupeFilter(RFPDupeFilter):
    """
    Redis-bloom request duplicates filter for redis-spider.
    This class can also be used with default Scrapy's scheduler.
    """

    def __init__(self, server, key, debug=False, **kwargs):
        super().__init__(server, key, debug)
        spider_settings = kwargs.get('spider_settings')
        if not spider_settings:
            raise EnvironmentError(
                "Please ensure you are using 'scrapy_ddiy.utils.scheduler.SchedulerDdiy' as the SCHEDULER.")

        self.server = Client(host=spider_settings.get('REDIS_HOST'), port=spider_settings.get('REDIS_PORT'),
                             **spider_settings.get('REDIS_PARAMS'))
        assert self.server.ping(), 'Redis failed to establish a connection, please check the settings'
        error_rate = spider_settings.getfloat('REDIS_BLOOM_ERROR_RATE')
        capacity = spider_settings.getint('REDIS_BLOOM_CAPACITY')
        assert capacity, "Please set the 'REDIS_BLOOM_CAPACITY' for the spider"
        assert error_rate, "Please set the 'REDIS_BLOOM_ERROR_RATE' for the spider"
        if not self.server.keys(self.key):
            try:
                # By default, bloom-filter is auto-scaling
                self.server.bfCreate(self.key, error_rate, capacity)
            except redis.exceptions.ResponseError:
                raise EnvironmentError('The redis not loaded the redis-bloom module. See the doc [ xx ]')

    def request_seen(self, request):
        """Returns True if request was already seen"""
        fp = self.request_fingerprint(request)
        # This returns the number of values added, zero if already exists.
        added = self.server.bfAdd(self.key, fp)
        return added == 0
