# -*- coding: utf-8 -*-
import os

"""
default_settings for scrapy_ddiy
"""

env = os.environ
DOWNLOADER_MIDDLEWARES = {
    # UserAgentMiddleware 默认优先级：500
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    # RetryMiddleware 默认优先级：550
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'scrapy_ddiy.downloadermiddlewares.custom_user_agent.CustomUserAgentMiddleware': 501,
    'scrapy_ddiy.downloadermiddlewares.log_crawl.LogCrawlMiddleware': 510,
    'scrapy_ddiy.downloadermiddlewares.retry.RetryMiddleware': 550,
    # CheckMiddleware 须大于等于 551
    'scrapy_ddiy.downloadermiddlewares.check.CheckMiddleware': 551,
}

SPIDER_MIDDLEWARES = {
    # CatchParseErrorMiddleware 优先级须为最高，否则其 process_spider_exception 会重复执行（前面有几个就额外执行几次）
    'scrapy_ddiy.spidermiddlewares.catch_parse_error.CatchParseErrorMiddleware': 998,

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
REDIS_HOST = env.get('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(env.get('REDIS_PORT', 6379))
# redis.Redis 所需参数
# decode_responses 参数用于配置Redis连接是否自动解码，不可设置为 True
# scrapy_redis 使用的是非解码，故不能使用解码（默认为非解码，此处只是显示写出）
REDIS_PARAMS = {
    'password': env.get('REDIS_PASSWORD', None),
    'db': 10,
    # decode_responses 参数用于配置 Redis 连接是否自动解码，不可设置为 True
    # scrapy_redis 使用的是非解码，故不能使用解码（默认为非解码）
    # 'decode_responses': False,
}
# Whether cleanup redis queues, allows to pause/resume crawls.
SCHEDULER_PERSIST = False

# MongoDB 配置
# 存放数据的 MongoDB
MONGO_URI = env.get('MONGO_URI', '127.0.0.1:27017')
# MongoDB 默认存入的数据库库名
MONGO_DATABASE = 'scrapy_ddiy_test'
# pymongo.MongoClient 所需参数
MONGO_PARAMS = {
    'username': env.get('MONGO_USERNAME', None),
    'password': env.get('MONGO_PASSWORD', None),
    'authSource': env.get('MONGO_AUTH', 'admin'),
}
# 为数据库创建索引，如：{'index_1':pymongo.ASCENDING,'index_2':pymongo.DESCENDING,...}
MONGO_INDEX_DICT = {}
# 存放爬虫异常信息的 MongoDB
MONGO_URI_STATS = env.get('MONGO_URI_STATS', '127.0.0.1:27017')
MONGO_DATABASE_STATS = 'scrapy_ddiy_stats'
MONGO_COLLECTION_STATS = 'scrapy_ddiy_stats'
MONGO_COLLECTION_EXCEPTION = 'scrapy_ddiy_exception'
MONGO_PARAMS_STATS = {
    'username': env.get('MONGO_USERNAME_STATS', None),
    'password': env.get('MONGO_PASSWORD_STATS', None),
    'authSource': env.get('MONGO_AUTH_STATS', 'admin'),
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

# TODO: 钉钉机器人联系人 hash 名，保存用户名（如maida）和手机号（用于@某人）如：{'name':'phone_number',...}
# 此为进阶功能，可不配置
DING_TALK_BOT_CONTACTS = 'DingTalkBot:contacts'

# 出现解析异常是否关闭爬虫
CLOSE_SPIDER_WHEN_PARSED_ERROR = True

# 邮箱配置
MAIL_HOST = env.get('MAIL_HOST_DDIY', 'localhost')
MAIL_PORT = env.get('MAIL_PORT_DDIY', 25)
MAIL_FROM = env.get('MAIL_FROM_DDIY', 'scrapy@localhost')
MAIL_PASS = env.get('MAIL_PASS_DDIY')
# 用户 SMTP 验证，如：'xx@xx.com'
MAIL_USER = env.get('MAIL_USER_DDIY', 'scrapy@localhost')
MAIL_SSL = True
# 收信人列表 ['xx@xx.com',...]
MAIL_TO = env.get('MAIL_TO_DDIY', 'scrapy@localhost')
# 抄送人列表 ['xx@xx.com',...]
MAIL_CC = None

# RedisBloomDupeFilter only for for redis-spider
# SCHEDULER = 'scrapy_ddiy.utils.scheduler.SchedulerDdiy'
# DUPEFILTER_CLASS = 'scrapy_ddiy.utils.dupefilter.RedisBloomDupeFilter'
# REDIS_BLOOM_ERROR_RATE = 0.001
# REDIS_BLOOM_CAPACITY = 100000

# 自定义重试异常响应状态码
CUSTOM_RETRY_HTTP_CODE = 6001
