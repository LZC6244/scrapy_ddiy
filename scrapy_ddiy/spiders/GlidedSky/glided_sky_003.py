# -*- coding: utf-8 -*-
import os
from scrapy import Request
from scrapy_ddiy.utils.spiders.ddiy_base import DdiyBaseSpider


class GlidedSky003Spider(DdiyBaseSpider):
    name = 'glided_sky_003'
    description = 'GlidedSky  爬虫-IP屏蔽1'
    start_url = 'http://www.glidedsky.com/level/web/crawler-ip-block-1'
    first_page = True
    num_count = 0
    custom_settings = {
        'COOKIES_ENABLED': True,
        'RETRY_ENABLED': False,
        # 没必要跑那么快，以免给别人网站造成压力
        'DOWNLOAD_DELAY': 1,
        'CONCURRENT_REQUESTS': 5,
        # 无可用代理时，等待下次获取代理的时间间隔
        'INTERVAL_GET_PROXY': 15,
        'GLIDED_SKY_ENABLE_PROXY': True,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_ddiy.downloadermiddlewares.glided_sky_downloadmiddleware.GlidedSkyMiddleware': 589,
        },
    }
    handle_httpstatus_list = [500, 502, 503, 504, 522, 524, 408, 429, 403, 302]
    pid: int

    def custom_init(self, *args, **kwargs):
        self.pid = os.getpid()

    def start_requests(self):
        yield Request(url=self.start_url, callback=self.parse, meta={'set_proxy': True, 'origin_url': self.start_url})

    def parse(self, response, **kwargs):
        if response.status in self.handle_httpstatus_list:
            # 在此处无限重试，直到访问成功为止，因为少访问到网页最终计算出来的结果也将不对
            origin_url = response.meta.get('origin_url')
            self.logger.info(f'重试：{response.url}')
            yield Request(url=response.url, callback=self.parse, dont_filter=True,
                          meta={'set_proxy': True, 'origin_url': origin_url})
            return
        if self.first_page:
            self.first_page = False
            max_page_num = response.xpath('//ul[@class="pagination"]/li[@class="page-item"]/a/text()')[-2].get()
            max_page_num = int(max_page_num)
            for page_num in range(2, max_page_num + 1):
                url = f'{self.start_url}?page={page_num}'
                yield Request(url=url, callback=self.parse, meta={'set_proxy': True, 'origin_url': url})
        num_li = [int(i) for i in response.xpath('//div[@class="card-body"]//div[@class="col-md-1"]/text()').getall()]
        self.num_count += sum(num_li)
        # with open(f'{self.name}__{self.pid}.txt', 'a') as f:
        #     f.write(f'{response.url} => {num_li}\n')

    def closed(self, reason):
        self.logger.info(f'Sum or web number is {self.num_count}')
