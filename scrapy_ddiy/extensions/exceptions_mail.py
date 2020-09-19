# -*- coding: utf-8 -*-

from scrapy import signals
from scrapy.mail import MailSender


class ExceptionsMail(object):
    """发送异常邮件"""

    mailer: MailSender
    mail_to: list
    mail_cc: list
    spider_start_time: str

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        settings = crawler.settings
        ext.mail_to = settings.getlist('MAIL_TO')
        if not ext.mail_to:
            raise AttributeError("Please set the 'MAIL_TO' for the crawler")
        ext.mail_cc = settings.getlist('MAIL_CC')
        ext.mailer = MailSender.from_settings(settings)

        # connect the extension object to signals
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.handle_spider_error, signal=signals.spider_error)

        # return the extension object
        return ext

    def spider_opened(self, spider):
        setattr(spider, '_exceptions_mail_on', True)
        self.spider_start_time = spider.crawler.stats.get_value('start_time')

    def handle_spider_error(self, spider):
        exception_info = spider._exception_info
        exception_info.pop('response_info', None)
        exception_info['exception_id'] = exception_info.pop('_id', None)
        exception_info['spider_start_time'] = self.spider_start_time
        mail_subject = f'Spider-Warning:  {exception_info.get("exception_type")}'
        mail_body = '\n'.join(
            [f'<tr><td><font size="4">{k}</font></td><td><font size="4">{v}</font></td></tr>'.replace('\n', '<br>') for
             k, v in exception_info.items()])
        mail_body = '<table border="1">' + mail_body + '</table>'
        self.mailer.send(to=self.mail_to, subject=mail_subject, body=mail_body, cc=self.mail_cc, mimetype='text/html')
