# -*- coding: utf-8 -*-
import os
import sys
import json
from time import sleep
from DingTalkBot.bot import DingTalkBot

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from scrapy_ddiy.utils.common import get_redis_conn
from scrapy_ddiy.utils.project import get_project_settings

"""
钉钉聊天机器人提醒,推荐用来发送少量、紧急的消息
因为钉钉机器人限制每分钟最多20条消息，且过多消息刷屏可能会忽略重要消息
"""


def ding_talk_bot_notify(msg_interval=5):
    """
    发送钉钉告警消息
    :param msg_interval: 每条消息之间的发送间隔
    :return:
    """
    settings = get_project_settings()
    redis_conn = get_redis_conn(settings)
    web_hook = os.environ.get('DING_WEB_HOOK')
    ding_secret = os.environ.get('DING_SECRET')
    if not web_hook or not ding_secret:
        raise ValueError('Please check the "DING_WEB_HOOK" or "DING_SECRET" whether in environment variables.')
    ding_talk_bot = DingTalkBot(web_hook=web_hook, secret=ding_secret)
    redis_msg_name = settings.get('WARN_MESSAGES_LIST')
    failed_msg_name = settings.get('WARN_MESSAGES_LIST_FAILED')
    msg_s = redis_conn.lpop(redis_msg_name)
    while msg_s:
        msg = json.loads(msg_s)
        warn_msg = msg.get('warn_msg', '')
        title = f'{warn_msg[:15]}...' if len(warn_msg) > 15 else warn_msg
        warn_msg = '\n'.join([f'#### {k}\n> {v}' for k, v in msg.items()])
        try:
            ding_talk_bot.send_markdown(title=title, text=warn_msg)
        except Exception as e:
            redis_conn.rpush(failed_msg_name, msg_s)
            repr(e)
        sleep(msg_interval)
        msg_s = redis_conn.lpop(redis_msg_name)

    redis_conn.close()


if __name__ == '__main__':
    ding_talk_bot_notify()
