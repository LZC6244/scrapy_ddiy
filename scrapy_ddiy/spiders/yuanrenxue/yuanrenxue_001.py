# -*- coding: utf-8 -*-
import json
import subprocess
from scrapy import Request
from scrapy_ddiy import DdiyBaseSpider


def get_m():
    """获取加密参数m"""
    return subprocess.check_output(['node', 'scrapy_ddiy/scripts/js/yuanrenxue/001.js']).decode().strip()


class Yuanrenxue001(DdiyBaseSpider):
    name = 'yuanrenxue_001'
    description = '猿人学刷题平台-第1题js混乱源码'
    # 总价
    total_price = 0

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
