# -*- coding: utf-8 -*-
import re
from scrapy import Request
from collections import defaultdict
from scrapy_ddiy.utils.spiders.ddiy_base import DdiyBaseSpider


class GlidedSky007Spider(DdiyBaseSpider):
    name = 'glided_sky_007'
    description = 'GlidedSky  css反爬'
    custom_settings = {
        'COOKIES_ENABLED': True,
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_ddiy.spiders.GlidedSky.glided_sky_downloadmiddleware.GlidedSkyMiddleware': 589,
        },
    }
    num_count = 0
    find_num: re.Pattern

    def custom_init(self, *args, **kwargs):
        self.find_num = re.compile('-?\\d+')

    def start_requests(self):
        for page_num in range(1, 1001):
            url = f'http://www.glidedsky.com/level/web/crawler-css-puzzle-1?page={page_num}'
            yield Request(url=url, callback=self.parse, meta={'page_num': page_num})

    def parse(self, response, **kwargs):
        page_num = response.meta['page_num']
        style_str = response.xpath('//style/text()').get()
        num_map = defaultdict(dict)
        for num_class, k, v in re.findall('\\.(.*?) \\{ (.*?):(.*?) }', style_str):
            num_map[num_class][k] = v
        # 保存当前页面的数字组合的列表
        num_li = []
        aa = 0
        for div_num_col in response.xpath('//div[@class="col-md-1"]'):
            aa += 1
            num_class_li = [(i.xpath('./@class').get(), i.xpath('./text()').get()) for i in div_num_col.xpath('./div')]
            index = 0
            tmp_num_li = [None] * len(num_class_li)
            for num_class, num_text in num_class_li:
                num_class_before = f'{num_class}:before'
                if num_map.get(num_class_before):
                    tmp_num_li = [str(self.find_num.search(num_map.get(num_class_before).get('content')).group())]
                    break
                num_info = num_map.get(num_class)
                if num_info.get('opacity'):
                    tmp_num_li.pop()
                    continue
                tmp_num_li[index + int(self.find_num.search(num_info.get('left', '0')).group())] = num_text
                index += 1
            num_li.append(int(''.join(tmp_num_li)))
        self.num_count += sum(num_li)
        self.logger.info(f'[ page: {page_num} ] => {num_li}')

    def closed(self, reason):
        self.logger.info(f'Sum or web number is {self.num_count}')
