# -*- coding: utf-8 -*-
import os
import json
import redis
from runpy import run_path
from DingTalkBot.bot import DingTalkBot

"""
钉钉聊天机器人提醒
"""


def get_settings():
    """获取项目配置"""
    return run_path('../settings.py')


def get_redis_conn(settings):
    return redis.Redis(host=settings.get('REDIS_HOST'), port=settings.get('REDIS_PORT'),
                       **settings.get('REDIS_PARAMS'))


def ding_talk_bot_notify():
    settings = get_settings()
    redis_conn = get_redis_conn(settings)
    web_hook = os.environ.get('DING_WEB_HOOK')
    ding_secret = os.environ.get('DING_SECRET')
    if not web_hook or not ding_secret:
        raise ValueError('Please check the "DING_WEB_HOOK" or "DING_SECRET"')
    ding_talk_bot = DingTalkBot(web_hook=web_hook, secret=ding_secret)
    redis_msg_name = settings.get('DING_TALK_BOT_MESSAGES')
    msg_li = [i for i in redis_conn.lrange(redis_msg_name, 0, 100)]
    for msg_s in msg_li:
        msg = json.loads(msg_s)
        if msg.get('msg_type') == 'text':
            ding_talk_bot.send_text(content=msg.get('content'))
            redis_conn.lrem(redis_msg_name, 1, msg_s)
        else:
            raise ValueError(f'msg_type must be "text" or "markdown",not "{msg.get("msg_type")}"')

    redis_conn.close()


if __name__ == '__main__':
    ding_talk_bot_notify()
