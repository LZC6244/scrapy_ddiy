# -*- coding: utf-8 -*-
from scrapy import Request

from scrapy_ddiy.utils.spiders.ddiy_base import DdiyBaseSpider
from scrapy_ddiy.spiders.GlidedSky.get_glided_sky_cookie import GLIDED_SKY_COOKIE_SET_NAME


class GlidedSky001Spider(DdiyBaseSpider):
    name = 'glided_sky_001'
    description = 'GlidedSky  第1题'
    start_url = 'http://www.glidedsky.com/level/web/crawler-basic-1'
    custom_settings = {
        'COOKIES_ENABLED': True,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_ddiy.downloadermiddlewares.glided_sky_downloadmiddleware.GlidedSkyMiddleware': 812,
        },
    }
    cookies: dict

    def custom_init(self, *args, **kwargs):
        glidedsky_session = self.redis_cli.get(GLIDED_SKY_COOKIE_SET_NAME)
        if not glidedsky_session:
            raise ValueError(f'{GLIDED_SKY_COOKIE_SET_NAME} not exists')
        self.cookies = {'glidedsky_session': glidedsky_session.decode()}

    def start_requests(self):
        yield Request(url=self.start_url, cookies=self.cookies)

    def parse(self, response):
        all_number = [int(i) for i in
                      response.xpath('//div[@class="card-body"]//div[@class="col-md-1"]/text()').getall()]
        print(f'Sum or web number is {sum(all_number)}')
