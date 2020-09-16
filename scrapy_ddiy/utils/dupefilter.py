# -*- coding: utf-8 -*-
import logging
from redisbloom.client import Client
from scrapy_redis.dupefilter import RFPDupeFilter

logger = logging.getLogger(__name__)


class RedisBloomDupeFilter(RFPDupeFilter):
    """
    Redis-bloom request duplicates filter.
    This class can also be used with default Scrapy's scheduler.
    """

    def request_seen(self, request):
        """Returns True if request was already seen"""
        fp = self.request_fingerprint(request)
        # This returns the number of values added, zero if already exists.
        added = self.server.sadd(self.key, fp)
        return added == 0
