import random
from datetime import date
import time

from nonebot.plugin import on_keyword
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message
# 10    20    35   75  80   85     95   96   97   98   99    100
# 大吉－中吉－小吉－吉－半吉－末吉－末小吉－凶－小凶－半凶－末凶－大凶


def luck_simple(num):
    if num <= 10:
        return '大吉'
    elif num <= 20:
        return '中吉'
    elif num <= 35:
        return '小吉'
    elif num <= 75:
        return '吉'
    elif num <= 80:
        return '半吉'
    elif num <= 85:
        return '末吉'
    elif num <= 95:
        return '末小吉'
    else:
        return '凶'


dp = []
# 维护一个1s的队列，要求队首
# TODO(ztx): 抽象为rate_limiter


def frequent(qps=3) -> bool:
    if len(dp) == 0:
        return False
    ms = time.time()
    while len(dp) > 0 and ms-dp[0] > 1:
        dp.pop(0)
    if len(dp) >= qps:
        return True
    dp.append(ms)
    return False


divine = on_keyword(['divine', '占卜', '抽签', "运势"])


@divine.handle()
async def divine_handle(bot: Bot, event: Event):
    if frequent():
        return
    rnd = random.Random()
    rnd.seed(int(date.today().strftime("%y%m%d")) + int(event.get_user_id()))
    lucknum = rnd.randint(1, 100)
    message = Message(
        f'[CQ:at,qq={event.get_user_id()}]您的今日运势为《{luck_simple(lucknum)}》')
    await divine.send(message=message)
