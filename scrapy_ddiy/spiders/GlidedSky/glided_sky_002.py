# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy_ddiy.utils.spiders.ddiy_base import DdiyBaseSpider


class GlidedSky002Spider(DdiyBaseSpider):
    name = 'glided_sky_002'
    description = 'GlidedSky  爬虫-基础2'
    start_url = 'http://www.glidedsky.com/level/web/crawler-basic-2'
    first_page = True
    num_count = 0
    custom_settings = {
        'COOKIES_ENABLED': True,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_ddiy.downloadermiddlewares.glided_sky_downloadmiddleware.GlidedSkyMiddleware': 589,
        },
    }

    def start_requests(self):
        yield Request(url=self.start_url, callback=self.parse)

    def parse(self, response):
        if self.first_page:
            self.first_page = False
            max_page_num = response.xpath('//ul[@class="pagination"]/li[@class="page-item"]/a/text()')[-2].get()
            max_page_num = int(max_page_num)
            for page_num in range(2, max_page_num + 1):
                url = f'{self.start_url}?page={page_num}'
                yield Request(url=url, callback=self.parse)
        num_li = [int(i) for i in response.xpath('//div[@class="card-body"]//div[@class="col-md-1"]/text()').getall()]
        self.num_count += sum(num_li)

    def closed(self, reason):
        self.logger.info(f'Sum or web number is {self.num_count}')
