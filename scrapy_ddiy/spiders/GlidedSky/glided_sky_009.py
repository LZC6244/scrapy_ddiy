# -*- coding: utf-8 -*-
import re
import ast
import base64
from io import BytesIO
from scrapy import Request
from fontTools.ttLib import TTFont
from scrapy_ddiy.utils.spiders.ddiy_base import DdiyBaseSpider


class GlidedSky009Spider(DdiyBaseSpider):
    name = 'glided_sky_009'
    description = 'GlidedSky  字体反爬2'
    custom_settings = {
        'COOKIES_ENABLED': True,
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_ddiy.spiders.GlidedSky.glided_sky_downloadmiddleware.GlidedSkyMiddleware': 589,
        },
    }
    num_count = 0
    find_b64_font: re.Pattern

    def custom_init(self, *args, **kwargs):
        self.find_b64_font = re.compile(';base64,(.*?)\\)')

    def start_requests(self):
        for page_num in range(1, 1001):
            # for page_num in range(1, 2):
            url = f'http://www.glidedsky.com/level/web/crawler-font-puzzle-2?page={page_num}'
            yield Request(url=url, callback=self.parse, meta={'page_num': page_num})

    def parse(self, response, **kwargs):
        page_num = response.meta['page_num']
        num_li = []
        font = self.find_b64_font.search(response.xpath('//style/text()').get()).group(1)
        font = TTFont(BytesIO(base64.b64decode(font)))
        best_cmap = font.getBestCmap()
        tmp_num_li = response.xpath('//div[@class="row"]/div[@class="col-md-1"]/text()').getall()
        for tmp_num in tmp_num_li:
            tmp_li = []
            tmp_num = tmp_num.strip()
            for num in tmp_num:
                glyph_id = best_cmap.get(ast.literal_eval(num.encode('unicode_escape').decode().replace('\\u', '0x')))
                real_num = str(font.getGlyphID(glyph_id) - 1)
                tmp_li.append(real_num)
            num_li.append(int(''.join(tmp_li)))
        self.num_count += sum(num_li)
        self.logger.info(f'[ page: {page_num} ] => {num_li}')

    def closed(self, reason):
        self.logger.info(f'Sum or web number is {self.num_count}')
