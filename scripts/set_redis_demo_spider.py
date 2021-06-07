# -*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scrapy_ddiy.utils.common import get_redis_conn
from scrapy_ddiy.utils.project import get_project_settings

"""
为 Redis 示例爬虫（redis_demo_spider）灌入种子
"""


def main():
    settings = get_project_settings()
    redis_conn = get_redis_conn(settings)
    redis_conn.rpush('redis_demo_spider:start_urls', *[str(i) for i in range(20)])
    print('为 redis_demo_spider 灌入 20 个 种子完成...')
    redis_conn.close()


if __name__ == '__main__':
    main()
