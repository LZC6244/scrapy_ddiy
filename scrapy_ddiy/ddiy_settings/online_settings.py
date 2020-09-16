# -*- coding: utf-8 -*-
"""
online_settings for scrapy_ddiy
"""
import os

env = os.environ

LOG_LEVEL = 'INFO'

REDIS_PORT = int(env.get('REDIS_PORT', 6379))
REDIS_PARAMS = {
    'password': env.get('REDIS_PASSWORD', None),
    'db': 11,
}

# MongoDB 配置
MONGO_URI = env.get('MONGO_URI', '127.0.0.1:27017')
# MongoDB 默认存入的数据库库名
MONGO_DATABASE = 'scrapy_ddiy'
# pymongo.MongoClient 所需参数
MONGO_PARAMS = {
    'username': env.get('MONGO_USERNAME', None),
    'password': env.get('MONGO_PASSWORD', None),
    'authSource': env.get('MONGO_AUTH', 'admin'),
}
MONGO_URI_EXCEPTION = env.get('MONGO_URI_EXCEPTION', '127.0.0.1:27017')
MONGO_DATABASE_EXCEPTION = 'scrapy_ddiy_exception'
MONGO_COLLECTION_EXCEPTION = 'scrapy_ddiy_exception'
MONGO_PARAMS_EXCEPTION = {
    'username': env.get('MONGO_USERNAME_EXCEPTION', None),
    'password': env.get('MONGO_PASSWORD_EXCEPTION', None),
    'authSource': env.get('MONGO_AUTH_EXCEPTION', 'admin'),
}

EXTENSIONS = {
    'scrapy_ddiy.extensions.exceptions_mail.ExceptionsMail': 100,
}

Exceptions_Mail_ENABLED = True

MAIL_HOST = env.get('MAIL_HOST_DDIY', 'localhost')
MAIL_PORT = env.get('MAIL_PORT_DDIY', 25)
MAIL_FROM = env.get('MAIL_FROM_DDIY', 'scrapy@localhost')
MAIL_PASS = env.get('MAIL_PASS_DDIY')
