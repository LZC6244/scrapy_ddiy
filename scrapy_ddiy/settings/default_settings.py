# -*- coding: utf-8 -*-
"""
default_settings for scrapy_ddiy
"""

DOWNLOADER_MIDDLEWARES = {
    # 默认优先级：500
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_ddiy.DownloadMiddlewares.CustomUserAgent.CustomUserAgent': 501,
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
    'backupCount': 0,
}
# 启用日志时是否保留控制台的输出
LOG_TO_CONSOLE = True

# 是否启用随机UA
RANDOM_UA = True
