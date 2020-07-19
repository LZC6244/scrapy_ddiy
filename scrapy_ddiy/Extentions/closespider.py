# -*- coding: utf-8 -*-


from collections import defaultdict
from scrapy import signals
from scrapy.exceptions import NotConfigured
from datetime import timedelta
from scrapy_ddiy.Extentions.mail import EmailSender


class CloseSpider(object):

    def __init__(self, crawler):
        self.crawler = crawler

        self.close_on = {
            'timeout': crawler.settings.getfloat('CLOSESPIDER_TIMEOUT'),
            'itemcount': crawler.settings.getint('CLOSESPIDER_ITEMCOUNT'),
            'pagecount': crawler.settings.getint('CLOSESPIDER_PAGECOUNT'),
            'errorcount': crawler.settings.getint('CLOSESPIDER_ERRORCOUNT'),
        }

        if not any(self.close_on.values()):
            raise NotConfigured

        self.counter = defaultdict(int)

        if self.close_on.get('errorcount'):
            crawler.signals.connect(self.error_count, signal=signals.spider_error)
        if self.close_on.get('pagecount'):
            crawler.signals.connect(self.page_count, signal=signals.response_received)
        if self.close_on.get('timeout'):
            crawler.signals.connect(self.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(self.spider_closed, signal=signals.spider_closed)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def send_mail(self, crawler, content):

        email = EmailSender(
            email_host=crawler.settings.get('MAIL_HOST'),
            email_pass=crawler.settings.get('MAIL_PASS'))
        content = content
        email.init(from_addr=crawler.settings.get('MAIL_FROM'),
                   to_addrs=crawler.settings.get('STATSMAILER_RCPTS'),
                   subject=crawler.settings.get('PROJECT_NAME'))
        email.attach_text(text=content)
        # email.attach_file(r'C:\xxx\xx.jpg')
        log_file = crawler.settings.get('LOG_FILE')
        if log_file:
            email.attach_file(log_file)
        email.send()
        email.close()

    def error_count(self, failure, response, spider):
        self.counter['errorcount'] += 1
        if self.counter['errorcount'] == self.close_on['errorcount']:
            self.crawler.engine.close_spider(spider, 'closespider_errorcount')

    def page_count(self, response, request, spider):
        self.counter['pagecount'] += 1
        if self.counter['pagecount'] == self.close_on['pagecount']:
            self.crawler.engine.close_spider(spider, 'closespider_pagecount')

    def item_scraped(self, item, spider):
        self.counter['itemcount'] += 1
        if self.counter['itemcount'] == self.close_on['itemcount']:
            self.crawler.engine.close_spider(spider, 'closespider_itemcount')

    def spider_closed(self, spider):
        task = getattr(self, 'task', False)
        if task and task.active():
            task.cancel()
        spider_stats = self.crawler.stats.get_stats(spider)
        lo = dict(spider_stats.items())
        lo['start_time'] = lo['start_time'] + timedelta(hours=8)
        lo['finish_time'] = lo['finish_time'] + timedelta(hours=8)
        content = "\n\n[ %s ] stats\n\n" % spider.name + "\n".join("%-50s : %s" % i for i in lo.items())
        self.send_mail(self.crawler, content)
