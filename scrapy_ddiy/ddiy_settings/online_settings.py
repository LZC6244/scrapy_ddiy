# -*- coding: utf-8 -*-
"""
online_settings for scrapy_ddiy
"""
import os

LOG_LEVEL = 'INFO'

REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
REDIS_PARAMS = {
    'password': os.environ.get('REDIS_PASSWORD', None),
    'db': 11,
}

# MongoDB 配置
MONGO_URI = os.environ.get('MONGO_URI', '127.0.0.1:27017')
# MongoDB 默认存入的数据库库名
MONGO_DATABASE = 'scrapy_ddiy'
# pymongo.MongoClient 所需参数
MONGO_PARAMS = {
    'username': os.environ.get('MONGO_USERNAME', None),
    'password': os.environ.get('MONGO_PASSWORD', None),
    'authSource': os.environ.get('MONGO_AUTH', 'admin'),
}
MONGO_URI_EXCEPTION = os.environ.get('MONGO_URI_EXCEPTION', '127.0.0.1:27017')
MONGO_DATABASE_EXCEPTION = 'scrapy_ddiy_exception'
MONGO_COLLECTION_EXCEPTION = 'scrapy_ddiy_exception'
MONGO_PARAMS_EXCEPTION = {
    'username': os.environ.get('MONGO_USERNAME_EXCEPTION', None),
    'password': os.environ.get('MONGO_PASSWORD_EXCEPTION', None),
    'authSource': os.environ.get('MONGO_AUTH_EXCEPTION', 'admin'),
}
