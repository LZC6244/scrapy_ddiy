# -*- coding: utf-8 -*-
"""
启动、运行爬虫
"""
import sys
from scrapy_ddiy.utils.crawler import CustomCrawlerProcess
from scrapy.utils.project import get_project_settings


def run_spider(spider_name, install_root_handler: bool = True):
    settings = get_project_settings()
    process = CustomCrawlerProcess(settings, install_root_handler)
    process.crawl(spider_name)
    process.start()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        run_spider(sys.argv[1])
    else:
        run_spider('demo_spider')
