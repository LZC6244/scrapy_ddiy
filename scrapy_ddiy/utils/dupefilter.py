# -*- coding: utf-8 -*-
import redis
from redisbloom.client import Client
from scrapy_redis.spiders import RedisSpider
from scrapy_redis.dupefilter import RFPDupeFilter

from scrapy_ddiy.utils.common import get_redis_conn
from scrapy_ddiy.utils.project import get_project_settings


class RedisBloomDupeFilter(RFPDupeFilter):
    """
    Redis-bloom request duplicates filter for redis-spider.
    This class can also be used with default Scrapy's scheduler.
    """

    def __init__(self, server, key, debug=False):
        super().__init__(server, key, debug)
        settings = get_project_settings()
        self.server = Client(host=settings.get('REDIS_HOST'), port=settings.get('REDIS_PORT'),
                             **settings.get('REDIS_PARAMS'))
        error_rate = settings.getfloat('REDIS_BLOOM_ERROR_RATE')
        capacity = settings.getfloat('REDIS_BLOOM_CAPACITY')
        assert error_rate, "Please set the 'REDIS_BLOOM_ERROR_RATE' for the spider"
        assert capacity, "Please set the 'REDIS_BLOOM_CAPACITY' for the spider"
        if not self.server.keys(key):
            try:
                self.server.bfCreate(key, error_rate, capacity)
            except redis.exceptions.ResponseError:
                raise EnvironmentError('The redis not loaded the redis-bloom module. See the doc [ xx ]')

    def request_seen(self, request):
        """Returns True if request was already seen"""
        fp = self.request_fingerprint(request)
        # This returns the number of values added, zero if already exists.
        added = self.server.sadd(self.key, fp)
        return added == 0
