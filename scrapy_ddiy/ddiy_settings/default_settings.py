# -*- coding: utf-8 -*-
"""
default_settings for scrapy_ddiy
"""

DOWNLOADER_MIDDLEWARES = {
    # UserAgentMiddleware 默认优先级：500
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_ddiy.downloadermiddlewares.custom_user_agent.CustomUserAgent': 501,
    'scrapy_ddiy.downloadermiddlewares.log_crawl.LogCrawl': 510,
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
# decode_responses 参数用于配置Redis连接是否自动解码，不可设置为 True
# scrapy_redis 使用的是非解码，故不能使用解码（默认为非解码，此处只是显示写出）
REDIS_PARAMS = {
    'password': None,
    'db': 10,
    # decode_responses 参数用于配置 Redis 连接是否自动解码，不可设置为 True
    # scrapy_redis 使用的是非解码，故不能使用解码（默认为非解码）
    # 'decode_responses': False,
}
# Whether cleanup redis queues, allows to pause/resume crawls.
SCHEDULER_PERSIST = False

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
# Redis 爬虫获取不到种子达到指定次数后关闭爬虫
IDLE_TIMES_MAX = 5
# 记录开始爬取请求
LOG_CRAWLING = True
# 记录开始解析响应
LOG_PARSING = True

# 钉钉机器人联系人 hash 名，保存用户名（如maida）和手机号（用于@某人）如：{'name':'phone_number',...}
# 此为进阶功能，可不配置
DING_TALK_BOT_CONTACTS = 'DingTalkBot:contacts'
# scrapy_ddiy 告警消息（预警/通知/自定义）的 list 名，如：[]
WARN_MESSAGES_LIST = 'scrapy_ddiy:warn_messages'
WARN_MESSAGES_LIST_FAILED = 'scrapy_ddiy:warn_messages_failed'
