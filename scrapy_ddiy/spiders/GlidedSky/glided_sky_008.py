# -*- coding: utf-8 -*-
import re
import base64
from io import BytesIO
from scrapy import Request
from fontTools.ttLib import TTFont
from scrapy_ddiy.utils.spiders.ddiy_base import DdiyBaseSpider


class GlidedSky008Spider(DdiyBaseSpider):
    name = 'glided_sky_008'
    description = 'GlidedSky 字体反爬1'
    custom_settings = {
        'COOKIES_ENABLED': True,
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_ddiy.spiders.GlidedSky.glided_sky_downloadmiddleware.GlidedSkyMiddleware': 589,
        },
    }
    num_count = 0
    num_map = {
        '0': 'zero',
        '1': 'one',
        '2': 'two',
        '3': 'three',
        '4': 'four',
        '5': 'five',
        '6': 'six',
        '7': 'seven',
        '8': 'eight',
        '9': 'nine',
    }
    find_b64_font: re.Pattern

    def custom_init(self, *args, **kwargs):
        self.find_b64_font = re.compile(';base64,(.*?)\\)')

    def start_requests(self):
        for page_num in range(1, 1001):
            url = f'http://www.glidedsky.com/level/web/crawler-font-puzzle-1?page={page_num}'
            yield Request(url=url, callback=self.parse, meta={'page_num': page_num})

    def parse(self, response, **kwargs):
        page_num = response.meta['page_num']
        num_li = []
        font = self.find_b64_font.search(response.xpath('//style/text()').get()).group(1)
        font = TTFont(BytesIO(base64.b64decode(font)))
        best_cmap = font.getBestCmap()
        current_num_map = dict()
        for i in best_cmap.values():
            real_num = str(font.getGlyphID(i) - 1)
            current_num_map[i] = real_num
        tmp_num_li = response.xpath('//div[@class="row"]/div[@class="col-md-1"]/text()').getall()
        for tmp_num in tmp_num_li:
            tmp_li = []
            tmp_num = tmp_num.strip()
            for num in tmp_num:
                tmp_li.append(current_num_map[self.num_map[num]])
            num_li.append(int(''.join(tmp_li)))
        self.num_count += sum(num_li)
        self.logger.info(f'[ page: {page_num} ] => {num_li}')

    def closed(self, reason):
        self.logger.info(f'Sum or web number is {self.num_count}')
