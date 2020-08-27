# -*- coding: utf-8 -*-
"""
default_settings for scrapy_ddiy
"""

DOWNLOADER_MIDDLEWARES = {
    # UserAgentMiddleware 默认优先级：500
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_ddiy.downloadermiddlewares.CustomUserAgent.CustomUserAgent': 501,
}

# 日志配置
LOG_LEVEL = 'INFO'
LOG_ENCODING = 'utf-8'
LOG_TIME_ROTATING = True
LOG_ROTATING_CFG = {
    # S - Seconds
    # M - Minutes
    # H - Hours
    # D - Days
    # midnight - roll over at midnight
    'when': 'midnight',
    'interval': 1,
    # 最大保留最新日志文件数，0 表示不限制
    'backupCount': 3,
}
# 启用日志时是否保留控制台的输出
LOG_TO_CONSOLE = True
# 是否生成日志文件
MAKE_LOG_FILE = True

# 是否启用随机UA
RANDOM_UA = True

# Redis 配置
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
# redis.Redis 所需参数
REDIS_PARAMS = {
    'password': None,
    'db': 10,
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

# 批量保存入库的 item 数
BULK_INSERT = 5
# 禁用 Telnet Console （scrapy 默认启用，Telnet 使用明文传输，不安全）
TELNETCONSOLE_ENABLED = False
