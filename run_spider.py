# -*- coding: utf-8 -*-
# @Author: lzc
# @Time  : 2020/6/15
# @Github: https://github.com/LZC6244
# @Desc  : 启动、运行爬虫
import subprocess
from scrapy_ddiy.utils.crawler import CustomCrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    settings = get_project_settings()

    run_spider(settings, True, 'test1')


def run_spider(settings, install_root_handler: bool, spider_name):
    process = CustomCrawlerProcess(settings, install_root_handler)
    # process = CrawlerProcess(settings, install_root_handler)
    process.crawl(spider_name)
    process.start()
    pass


if __name__ == '__main__':
    main()
