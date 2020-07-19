# -*- coding: utf-8 -*-
"""
测试启动、运行爬虫
"""
import os
import subprocess
from scrapy_ddiy.utils.crawler import CustomCrawlerProcess
import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from scrapy import cmdline
from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from concurrent.futures import ProcessPoolExecutor


def main():
    os.chdir('..')
    settings = get_project_settings()

    # sub_process = subprocess.run(['scrapy', 'list'], capture_output=True)
    # spiders_li = sub_process.stdout.decode().split()
    # 参考 https://docs.scrapy.org/en/latest/topics/practices.html?highlight=CrawlerProcess#run-scrapy-from-a-script
    # process = CrawlerProcess(settings)
    # process.crawl('test1')
    # process.crawl('test2')
    # process.start()
    # cmdline.execute('scrapy crawl test1'.split())

    # custom_log2(settings, ['test1'])
    # subprocess.run('scrapy crawl test1'.split(), capture_output=True)
    # subprocess.run('scrapy crawl test2'.split(), capture_output=True)

    # executor = ProcessPoolExecutor(max_workers=3)
    # executor.submit(run_spider, settings, True, 'test1')
    # # executor.submit(run_spider, settings, True, 'test2')
    # executor.shutdown(wait=True)

    run_spider(settings, True, 'test1')


def run_spider(settings, install_root_handler: bool, spider_name):
    process = CustomCrawlerProcess(settings, install_root_handler)
    # process = CrawlerProcess(settings, install_root_handler)
    process.crawl(spider_name)
    process.start()
    pass


if __name__ == '__main__':
    main()
