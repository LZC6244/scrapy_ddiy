# -*- coding: utf-8 -*-
import os
import scrapy
from time import sleep
from datetime import datetime

"""
scrapy_ddiy 基本爬虫
"""


class DdiyBaseSpider(scrapy.Spider):
    name = 'ddiy_base'

    # allowed_domains = ['base']
    start_urls = ['https://www.baidu.com/']

    # custom_settings 优先级高于 ddiy_settings
    ddiy_settings = {
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 1,
    }

    @classmethod
    def update_settings(cls, settings):
        now = datetime.now().strftime('%Y-%m-%dT%H_%M_%S')
        log_file = settings.get('LOG_FILE') or f'spider_logs/{cls.name}/{cls.name}__{now}__{os.getpid()}.log'
        # log_file = f'spider_logs/{cls.name}/{cls.name}__{now}__{os.getpid()}.log'
        make_log_dir(log_file)
        settings.setdict({'LOG_FILE': log_file}, priority='spider')
        settings.setdict(cls.ddiy_settings or {}, priority='spider')
        settings.setdict(cls.custom_settings or {}, priority='spider')

    def custom_init(self, *args, **kwargs):
        self.logger.info('h' * 30)
        # self.make_log_dir(self.settings.get('LOG_FILE'))

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        spider.custom_init(*args, **kwargs)
        return spider

    def parse(self, response):
        self.logger.info('hello scrapy.')
        sleep(1.5)
        self.logger.warning('hhhhhhhhh')
        print(response.request.headers['User-Agent'])


def make_log_dir(log_file: str = None):
    if not log_file:
        return
    current_dir = os.path.dirname(__file__)
    log_dir = os.path.join(current_dir, '../../..', os.path.split(log_file)[0])
    os.makedirs(log_dir, exist_ok=True)
    # print(os.path.normpath(log_dir))
