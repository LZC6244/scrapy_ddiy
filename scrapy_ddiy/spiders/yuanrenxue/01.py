# -*- coding: utf-8 -*-
import json
import subprocess
from scrapy import Request
from scrapy_ddiy.utils.spiders.ddiy_base import DdiyBaseSpider


def get_m():
    """获取加密参数m"""
    return subprocess.check_output(['node', 'scrapy_ddiy/scripts/js/yuanrenxue/01.js']).decode().strip()


class Yuanrenxue01(DdiyBaseSpider):
    name = 'yuanrenxue_01'
    description = '猿人学刷题平台-第一题js混乱源码'
    # 总价
    total_price = 0
    custom_settings = {'COOKIES_ENABLED': True}

    def start_requests(self):
        headers = {'User-Agent': 'yuanrenxue.project'}
        for i in range(1, 6):
            m = get_m()
            url = f'http://match.yuanrenxue.com/api/match/1?page={i}&m={m}'
            yield Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response, **kwargs):
        data = json.loads(response.text).get('data')
        num_li = [i.get('value') for i in data]
        self.logger.info(num_li)
        self.total_price += sum(num_li)

    def closed(self, reason):
        self.logger.info(f'总价为：{self.total_price}')
        super().closed(reason)
