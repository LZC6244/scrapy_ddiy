# -*- coding: utf-8 -*-
import os
import re
import json
import redis
import pymongo
from scrapy import Spider
from datetime import datetime
from scrapy.mail import MailSender
from scrapy.item import Item, Field
from scrapy.settings import Settings, BaseSettings

from scrapy_ddiy.utils.common import get_request_md5, get_local_ip

"""
scrapy_ddiy 基础爬虫
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
    # 预设给爬虫使用的 MongoDB 连接，用于记录爬虫异常信息
    mongo_cli_exec: pymongo.MongoClient
    mongo_coll_exec: pymongo.collection.Collection
    # 本机内网 IP
    _local_ip: str
    # 是否为线上环境
    is_online: bool

    # 邮件配置
    mail_to: str
    mail_cc: str
    mail_sender: MailSender
    _init_mailer: bool

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
        self._local_ip = get_local_ip()
        self.is_online = os.environ.get('ENV_FLAG_DDIY') == 'online'
        if self.is_online:
            # 仅在正式环境启用异常记录，应尽可能在开发爬虫时处理完异常情况
            self.mongo_cli_exec = pymongo.MongoClient(self.settings.get('MONGO_URI_EXCEPTION'),
                                                      **self.settings.getdict('MONGO_PARAMS_EXCEPTION'))
            self.mongo_coll_exec = self.mongo_cli_exec[self.settings.get('MONGO_DATABASE_EXCEPTION')][
                self.settings.get('MONGO_COLLECTION_EXCEPTION')]
            index_name_li = list(self.mongo_coll_exec.index_information().keys())
            index_name = 'warn_time'
            index_exists = False
            for i in index_name_li:
                if re.search(f'{index_name}_-?1', i):
                    index_exists = True
                    break
            if not index_exists:
                self.mongo_coll_exec.create_index([(index_name, self.settings.get('MONGO_INDEX_ASC'))],
                                                  expireAfterSeconds=self.settings.getint('EXCEPTION_EXPIRE',
                                                                                          15) * 24 * 60 * 60)
        else:
            # 防止开发爬虫时污染线上数据
            self.logger.info('Non-online environment! Set the database table name to "scrapy_ddiy_test"')
            self.table_name_ddiy = 'scrapy_ddiy_test'

        if self.settings.getbool('ENABLE_MAIL'):
            self.mail_to = self.settings.getlist('MAIL_TO')
            assert self.mail_to, "Please set the 'MAIL_TO' for the spider"
            self.mail_cc = self.settings.getlist('MAIL_CC')
            self.mail_sender = MailSender.from_settings(self.settings)
            if self.mail_sender.smtphost == 'localhost':
                raise AttributeError(
                    'Please set the settings like [https://doc.scrapy.org/en/latest/topics/email.html#mail-settings]')
            self._init_mailer = True

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        spider.base_init(*args, **kwargs)
        spider.custom_init(*args, **kwargs)
        if spider.is_online:
            assert spider.mongo_cli_exec.server_info(), 'MongoDB for logging exceptions  failed to establish a ' \
                                                        'connection, please check the settings '
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

    def send_ding_bot_msg(self, warn_msg: str):
        time_format = '%Y-%m-%d %H:%M:%S'
        start_time = self.crawler.stats.get_stats()['start_time'].strftime(time_format)
        warn_time = datetime.now().strftime(time_format)
        msg_dict = {'start_time': start_time, 'warn_time': warn_time,
                    'spider_name': f'[{self.name}] {self.description}', 'warn_msg': warn_msg,
                    'server_ip': self._local_ip, 'pid': os.getpid()}
        self.crawler.stats.inc_value('warn_msg_count/ding_bot')
        self.redis_cli.rpush(self.settings.get('WARN_MESSAGES_LIST'), json.dumps(msg_dict, ensure_ascii=False))

    def send_mail(self, warn_type: str, warn_msg: str or dict):
        if not getattr(self, '_init_mailer', False):
            raise UserWarning("Can't use 'send_mail' when 'ENABLE_MAIL' is not True")
        mail_subject = f'Spider-Warning:  {warn_type}'
        if isinstance(warn_msg, dict):
            mail_body = '\n'.join(
                [f'<tr><td><font size="4">{k}</font></td><td><font size="4">{v}</font></td></tr>'.replace('\n', '<br>')
                 for k, v in warn_msg.items()])
            mail_body = '<table border="1">' + mail_body + '</table>'
            mime_type = 'text/html'
        elif isinstance(warn_msg, str):
            mail_body = warn_msg
            mime_type = 'text/plain'
        else:
            raise AttributeError("'warn_msg' must be str or dict")
        self.mail_sender.send(to=self.mail_to, subject=mail_subject, body=mail_body, cc=self.mail_cc,
                              mimetype=mime_type)

    def closed(self, reason):
        if self.is_online:
            self.mongo_cli_exec.close()
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
