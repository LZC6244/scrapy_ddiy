# -*- coding: utf-8 -*-

import logging
from scrapy import signals
from scrapy.mail import MailSender

logger = logging.getLogger(__name__)


class ExceptionsMail(object):
    """发送异常邮件"""

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        ext.mailer = MailSender.from_settings(crawler.settings)

        # connect the extension object to signals
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.handle_spider_error, signal=signals.spider_error)

        # return the extension object
        return ext

    def spider_opened(self, spider):
        setattr(spider, '_exceptions_mail_on', True)

    def handle_spider_error(self, spider):
        pass
