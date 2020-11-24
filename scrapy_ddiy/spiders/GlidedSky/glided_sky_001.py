# -*- coding: utf-8 -*-
from scrapy import Request

from scrapy_ddiy.utils.spiders.ddiy_base import DdiyBaseSpider


class GlidedSky001Spider(DdiyBaseSpider):
    name = 'glided_sky_001'
    description = 'GlidedSky  爬虫-基础1'
    start_url = 'http://www.glidedsky.com/level/web/crawler-basic-1'
    custom_settings = {
        'COOKIES_ENABLED': True,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_ddiy.downloadermiddlewares.glided_sky_downloadmiddleware.GlidedSkyMiddleware': 589,
        },
    }

    def start_requests(self):
        yield Request(url=self.start_url, callback=self.parse)

    def parse(self, response, **kwargs):
        all_number = [int(i) for i in
                      response.xpath('//div[@class="card-body"]//div[@class="col-md-1"]/text()').getall()]
        self.logger.info(f'Sum or web number is {sum(all_number)}')
