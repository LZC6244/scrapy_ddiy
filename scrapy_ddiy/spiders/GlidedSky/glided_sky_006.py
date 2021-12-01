# -*- coding: utf-8 -*-
import re
import math
from scrapy import Request
from scrapy_ddiy.utils.spiders.ddiy_base import DdiyBaseSpider


class GlidedSky006Spider(DdiyBaseSpider):
    name = 'glided_sky_006'
    description = 'GlidedSky 雪碧图1'
    custom_settings = {
        'COOKIES_ENABLED': True,
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_ddiy.spiders.GlidedSky.glided_sky_downloadmiddleware.GlidedSkyMiddleware': 589,
        },
    }
    num_count = 0

    def start_requests(self):
        for page_num in range(1, 1001):
            url = f'http://www.glidedsky.com/level/web/crawler-sprite-image-1?page={page_num}'
            yield Request(url=url, callback=self.parse, meta={'page_num': page_num})

    def parse(self, response, **kwargs):
        page_num = response.meta['page_num']
        style_str = response.xpath('//style/text()').get()
        num_info = {num_map: background_position_x for num_map, background_position_x in
                    re.findall('\\.(.*?) .*?background-position-x:(-?\\d+)px', style_str)}
        background_position_x_li = sorted(set(num_info.values()), key=lambda x: abs(int(x)))
        # 首个必定为 0 （当本页数字组成无 0 时会缺失 0）
        if '0' not in background_position_x_li:
            background_position_x_li = ['0'] + background_position_x_li
        tmp_position_x = 0
        current_num = 0
        # background_position_x 和 数字的映射，如 "background-position-x: -70px" 映射为数字 6
        position_map_num = {'0': 0}
        for position_x in background_position_x_li[1:]:
            current_num += 1
            # 前一个数和后一个数相差多少个 15 （向上取整）
            # 超过一个 15 说明本页数字无需完整 0-9 即可组成，此时需要进行补全方便进行数字的映射
            diff_num = math.ceil((tmp_position_x - int(position_x)) / 15)
            for i in range(diff_num - 1):
                tmp_position_x -= 15
                position_map_num[str(tmp_position_x)] = current_num
                current_num += 1
            position_map_num[position_x] = current_num
            tmp_position_x = int(position_x)
        num_li = []
        for num_column in response.xpath('//div[@class="row"]/div[@class="col-md-1"]'):
            tmp_num = ''
            for i in num_column.xpath('./div/@class').getall():
                i = i.replace(' sprite', '')
                tmp_num += str(position_map_num[num_info[i]])
            num_li.append(int(tmp_num))
        self.num_count += sum(num_li)
        self.logger.info(f'[ page: {page_num} ] => {num_li}')

    def closed(self, reason):
        self.logger.info(f'Sum or web number is {self.num_count}')
