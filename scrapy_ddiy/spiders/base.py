# -*- coding: utf-8 -*-
import scrapy
import logging
from scrapy.utils.log import configure_logging

from scrapy_ddiy.settings import LOG_DIR


class BaseSpider(scrapy.Spider):
    name = 'base'

    # allowed_domains = ['base']
    start_urls = ['https://www.baidu.com/']

    # custom_settings 优先级高于 ddiy_settings
    ddiy_settings = {
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 1.5,
    }

    @property
    def logger(self):
        # configure_logging(install_root_handler=False)

        return logging.getLogger('lzc')

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(cls.ddiy_settings or {}, priority='spider')
        settings.setdict(cls.custom_settings or {}, priority='spider')

    def parse(self, response):
        self.logger.info('hello scrapy.')
        self.logger.warning('hhhhhhhhh')
        print(response.request.headers['User-Agent'])
