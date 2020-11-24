# -*- coding: utf-8 -*-
import json
from scrapy import FormRequest
from scrapy_ddiy.utils.common import get_str_md5
from scrapy_ddiy.utils.spiders.ddiy_base import DdiyBaseSpider

"""
ALAPI：QPS限制为3 , 每天限制请求100次
"""


class AlapiDogSpider(DdiyBaseSpider):
    description = 'ALAPI-舔狗日记'
    name = 'alapi_dog'
    start_url = 'https://v1.alapi.cn/api/dog'
    custom_settings = {
        'MAKE_LOG_FILE': False,
        'MONGO_DATABASE': 'ALAPI',
        'CONCURRENT_REQUESTS': 1,
        'BULK_INSERT': 10,
        'DOWNLOAD_DELAY': 2,
        'HTTPERROR_ALLOWED_CODES': [429],
        'ITEM_PIPELINES': {
            'scrapy_ddiy.pipelines.mongodb.MongodbPipeline': 300,
        }
    }

    def start_requests(self):
        form_data = {'format': 'json'}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        # 每次爬取 100 条
        for i in range(100):
            yield FormRequest(url=self.start_url, callback=self.parse, dont_filter=True,
                              headers=headers, formdata=form_data)

    def check_status(self, response):
        if response.status == 429:
            msg = '已达到访问频率限制，停止爬虫...'
            self.send_ding_bot_msg(msg)
            self.crawler.engine.close_spider(self, msg)
            return False
        return True

    def parse(self, response, **kwargs):
        if not self.check_status(response):
            return
        data = json.loads(response.text)
        content = data.get('data').get('content')
        item = {'_id': get_str_md5(content), 'content': content, 'sent_time': None}
        item = self.process_parsed_item(response, item)
        yield item

    def closed(self, reason):
        spider_stats = self.crawler.stats.get_stats()
        item_scraped_count = spider_stats.get('item_scraped_count', 0)
        if item_scraped_count <= 0 and reason == 'finished':
            warn_msg = f'共爬取 {item_scraped_count} 条数据，请检查...'
            self.send_ding_bot_msg(warn_msg=warn_msg)
        super().closed(reason)
