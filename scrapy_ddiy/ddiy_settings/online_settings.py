# -*- coding: utf-8 -*-
"""
online_settings for scrapy_ddiy
"""
import os

env = os.environ

LOG_LEVEL = 'INFO'

REDIS_PARAMS = {
    'password': env.get('REDIS_PASSWORD', None),
    'db': 11,
}
MONGO_DATABASE = 'scrapy_ddiy'
SCHEDULER_PERSIST = True
# 启用以下组件，方便发生解析异常等情况时重新灌入请求等
SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'

CLOSE_SPIDER_WHEN_PARSED_ERROR = False
