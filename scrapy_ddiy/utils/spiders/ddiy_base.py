# -*- coding: utf-8 -*-
import os
import redis
import pymongo
from scrapy import Spider
from datetime import datetime
from scrapy.mail import MailSender
from scrapy.item import Item, Field
from MsgBot import DingTalkBot
from scrapy.settings import Settings, BaseSettings

from scrapy_ddiy.utils.common import get_request_md5, get_local_ip

"""
scrapy_ddiy base spider
"""


class DdiyBaseSpider(Spider):
    name = 'ddiy_base'
    # 爬虫描述，必填
    description: str = None

    # 管道配置
    # 数据库表名
    table_name_ddiy = None

    # custom_settings 优先级高于 _ddiy_settings
    _ddiy_settings = {}
    # 预设给爬虫使用的 Redis 连接（如 scrapy_redis 、 记录告警信息）
    redis_cli: redis.Redis
    # 预设给爬虫使用的 MongoDB 连接，用于记录爬虫运行状态、异常信息等
    mongo_cli: pymongo.MongoClient
    mongo_coll_stats: pymongo.collection.Collection
    mongo_coll_exception: pymongo.collection.Collection
    # 本机内网 IP
    local_ip: str
    # 爬虫进程 ID
    pid: int
    # 是否为线上环境
    is_online: bool

    # 邮件配置
    mail_to: str
    mail_cc: str
    mail_sender: MailSender

    @classmethod
    def update_settings(cls, settings):
        now = datetime.now().strftime('%Y-%m-%dT%H_%M_%S')
        _update_settings(settings, cls._ddiy_settings or {}, priority='spider')
        _update_settings(settings, cls.custom_settings or {}, priority='spider')
        if settings.getbool('MAKE_LOG_FILE'):
            log_file = settings.get('LOG_FILE', f'spider_logs/{cls.name}/{cls.name}__{now}__{os.getpid()}.log')
            make_log_dir(log_file)
            settings.setdict({'LOG_FILE': log_file}, priority='spider')

    def custom_init(self, *args, **kwargs):
        pass

    def base_init(self, *args, **kwargs):
        self.redis_cli = getattr(self, 'server', None) or \
                         redis.Redis(host=self.settings.get('REDIS_HOST'), port=self.settings.get('REDIS_PORT'),
                                     **self.settings.getdict('REDIS_PARAMS'))
        self.local_ip = get_local_ip()
        self.is_online = os.environ.get('ENV_FLAG_DDIY') == 'online'
        self.mongo_cli = pymongo.MongoClient(self.settings.get('MONGO_URI_STATS'),
                                             **self.settings.getdict('MONGO_PARAMS_STATS'))
        self.mongo_coll_stats = self.mongo_cli[self.settings.get('MONGO_DATABASE_STATS')][
            self.settings.get('MONGO_COLLECTION_STATS')]
        self.mongo_coll_exception = self.mongo_cli[self.settings.get('MONGO_DATABASE_STATS')][
            self.settings.get('MONGO_COLLECTION_EXCEPTION')]
        self.mongo_coll_exception.create_index([('warn_time', pymongo.ASCENDING)],
                                               expireAfterSeconds=self.settings.getint('EXCEPTION_EXPIRE',
                                                                                       90) * 24 * 60 * 60)
        self.pid = os.getpid()

        self.mail_to = self.settings.getlist('MAIL_TO')
        assert self.mail_to, "Please set the 'MAIL_TO' for the spider"
        self.mail_cc = self.settings.getlist('MAIL_CC')
        self.mail_sender = MailSender.from_settings(self.settings)
        if self.mail_sender.smtphost == 'localhost':
            raise AttributeError(
                'Please set the settings like [https://doc.scrapy.org/en/latest/topics/email.html#mail-settings]')

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        spider.base_init(*args, **kwargs)
        spider.custom_init(*args, **kwargs)
        assert spider.mongo_cli.server_info(), 'MongoDB failed to establish a connection, please check the settings'
        assert spider.redis_cli.ping(), 'Redis failed to establish a connection, please check the settings'
        assert spider.description, 'Please fill in a description for the Spider, such as: "Sample Spider", ' \
                                   '"XX-Spider" ... '

        return spider

    @staticmethod
    def _adjust_item(parsed_item: dict):
        item = Item()
        for k, v in parsed_item.items():
            item.fields[k] = Field()
            item[k] = v
        return item

    def process_parsed_item(self, response, parsed_item: dict, set_id=True):
        """若同一个请求中解析出多条数据，请为每条数据手动设置 _id"""
        if set_id:
            # 默认不覆盖 parsed_item 中带过来的 _id
            parsed_item.setdefault('_id', get_request_md5(response.request))
        parsed_item['crawl_time'] = datetime.now()
        return self._adjust_item(parsed_item)

    def send_ding_bot_msg(self, content: str, at_mobiles: list = None, at_all=False, q_timeout: int = 60,
                          r_timeout: int = 60):
        """建议使用钉钉消息进行短内容消息推送，如cookie过期等"""
        web_hook = self.settings.get('DING_WEB_HOOK')
        secret = self.settings.get('DING_SECRET')
        if not web_hook or not secret:
            raise AttributeError('Please set the [DING_WEB_HOOK] and [DING_SECRET] for the spider/')
        dt_bot = DingTalkBot(web_hook=web_hook, secret=secret)
        dt_bot.send_text(content, at_mobiles, at_all, q_timeout, r_timeout)

    def send_mail(self, mail_subject: str, warn_msg: str or dict, **kwargs):
        """建议使用邮件来发送异常等长内容通知"""
        if isinstance(warn_msg, dict):
            kwargs = warn_msg
        elif isinstance(warn_msg, str):
            kwargs['warn_msg'] = warn_msg
        else:
            raise AttributeError("'warn_msg' must be a str or dict")
        mail_body = '\n'.join(
            [f'<tr><td><font size="4">{k}</font></td><td><font size="4">{v}</font></td></tr>'.replace('\n', '<br>')
             for k, v in kwargs.items()])
        mail_body = '<table border="1">' + mail_body + '</table>'
        mime_type = 'text/html'
        self.mail_sender.send(to=self.mail_to, subject=mail_subject, body=mail_body, cc=self.mail_cc,
                              mimetype=mime_type)

    def closed(self, reason):
        self.mongo_cli.close()
        self.redis_cli.close()


def make_log_dir(log_file: str = None):
    if not log_file:
        return
    current_dir = os.path.dirname(__file__)
    log_dir = os.path.join(current_dir, '../../..', os.path.split(log_file)[0])
    os.makedirs(log_dir, exist_ok=True)
    # print(os.path.normpath(log_dir))


def _update_settings(settings: Settings, new_settings: dict, priority='project'):
    for k, v in new_settings.items():
        old_k_value = settings.get(k)
        if isinstance(old_k_value, BaseSettings):
            old_k_value.update(v)
            v = old_k_value
        settings.set(k, v, priority)
