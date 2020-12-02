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
    # 是否保存异常到 MongoDB 且发送邮件
    save_and_send_exception: bool
    # 表明发送提醒消息的方法
    send_msg_method: str

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
        self.save_and_send_exception = self.settings.getbool('SAVE_AND_SEND_EXCEPTION')
        self.send_msg_method = self.settings.get('SEND_MSG_METHOD')
        if self.save_and_send_exception:
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
        if self.is_online:
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
        if spider.save_and_send_exception:
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

    def send_ding_bot_msg(self, warn_type, start_time, warn_time, spider_name, server_ip, pid,
                          exception_id=None, warn_msg: str = None, up_kwargs: bool = False, **kwargs):
        msg_dict = {'spider_name': spider_name, 'warn_type': warn_type, 'start_time': start_time,
                    'warn_time': warn_time, 'server_ip': server_ip, 'pid': pid}
        if exception_id:
            msg_dict['exception_id'] = exception_id
        if warn_msg:
            msg_dict['warn_msg'] = warn_msg
        if up_kwargs:
            msg_dict.update(**kwargs)
        self.crawler.stats.inc_value('warn_msg_count/ding_bot')
        self.redis_cli.rpush(self.settings.get('WARN_MESSAGES_LIST'), json.dumps(msg_dict, ensure_ascii=False))

    def send_mail(self, warn_type: str, spider_name, warn_msg: str or dict, **kwargs):
        if not getattr(self, '_init_mailer', False):
            raise UserWarning("Can't use 'send_mail' when 'SAVE_AND_SEND_EXCEPTION' is not True")
        mail_subject = f'Spider-Warning: [{warn_type}] {spider_name}'
        if isinstance(warn_msg, dict):
            kwargs = warn_msg
        elif isinstance(warn_msg, str):
            kwargs['warn_msg'] = warn_msg
        else:
            raise AttributeError("'warn_msg' must be str or dict")
        mail_body = '\n'.join(
            [f'<tr><td><font size="4">{k}</font></td><td><font size="4">{v}</font></td></tr>'.replace('\n', '<br>')
             for k, v in kwargs.items()])
        mail_body = '<table border="1">' + mail_body + '</table>'
        mime_type = 'text/html'
        self.mail_sender.send(to=self.mail_to, subject=mail_subject, body=mail_body, cc=self.mail_cc,
                              mimetype=mime_type)

    def send_msg(self, method: str, server_ip: str = None, **kwargs):
        """
        爬虫发送提醒消息的方法
        :param method: 发送方法，目前支持
                       {
                       'mail':邮件,
                       'dingding':钉钉
                       }
        :param server_ip: 服务器 ip
        :param kwargs:
        :return:
        """
        time_format = '%Y-%m-%d %H:%M:%S'
        start_time = self.crawler.stats.get_stats()['start_time'].strftime(time_format)
        warn_time = datetime.now().strftime(time_format)
        spider_name = f'[{self.name}] {self.description}'
        server_ip = server_ip or self._local_ip
        params_dict = {'start_time': start_time, 'warn_time': warn_time, 'spider_name': spider_name,
                       'server_ip': server_ip, 'pid': os.getpid()}
        params_dict.update(**kwargs)
        method = method.lower()
        if method == 'mail':
            return self.send_mail(**params_dict)
        elif method == 'dingding':
            return self.send_ding_bot_msg(**params_dict)
        else:
            raise ValueError("'method' must be one of ['mail', 'dingding']")

    def closed(self, reason):
        if self.save_and_send_exception:
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
