# -*- coding: utf-8 -*-
"""
online_settings for scrapy_ddiy
"""


REDIS_PARAMS = {
    'password': None,
    'db': 11,
    # Redis连接 是否自动解码
    'decode_responses': True,
}

# MongoDB 配置
MONGO_URI = '127.0.0.1:27017'
# MongoDB 默认存入的数据库库名
MONGO_DATABASE = 'scrapy_ddiy_test'
# pymongo.MongoClient 所需参数
MONGO_PARAMS = {
    'username': None,
    'password': None,
    'authSource': 'admin',
}