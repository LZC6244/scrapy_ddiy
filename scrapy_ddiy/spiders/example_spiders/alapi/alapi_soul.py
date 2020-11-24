# -*- coding: utf-8 -*-
import json
from scrapy import FormRequest
from scrapy_ddiy.utils.common import get_str_md5
from scrapy_ddiy.spiders.example_spiders.alapi.alapi_dog import AlapiDogSpider


class AlapiSoulSpider(AlapiDogSpider):
    name = 'alapi_soul'
    description = 'ALAPI-心灵毒鸡汤'
    start_url = 'https://v1.alapi.cn/api/soul'

    def start_requests(self):
        form_data = {'format': 'json'}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        # 每次爬取 100 条
        for i in range(100):
            yield FormRequest(url=self.start_url, callback=self.parse, dont_filter=True,
                              headers=headers, formdata=form_data)

    def parse(self, response, **kwargs):
        if not self.check_status(response):
            return
        data = json.loads(response.text)
        content = data.get('data').get('title')
        item = {'_id': get_str_md5(content), 'content': content, 'sent_time': None}
        item = self.process_parsed_item(response, item)
        yield item
