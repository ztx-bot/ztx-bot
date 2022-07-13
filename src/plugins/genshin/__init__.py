import genshin

from nonebot.plugin import on_keyword
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message
from config import get_config


genshin_data = on_keyword(['genshin_data', '原神'])

cfg = get_config('genshin')
api = genshin.api_v1.API_V1(cfg['cookie'])


@genshin_data.handle()
async def genshin_data_handle(bot: Bot, event: Event):
    try:
        uid = int(event.get_plaintext().split(' ')[1].strip())
    except:
        await genshin_data.send("uid错误")
        return
    if uid < 100000000:
        await genshin_data.send("uid太小了")
        return
    if uid > 999999999:
        await genshin_data.send("uid太大了")
        return
    try:
        data = api.index(uid)
        msg = f'''
{data.role.nickname}
等级: {data.role.level}
活跃天数: {data.stats.active_day_number}
成就数: {data.stats.achievement_number}
角色数量: {data.stats.avatar_number}
深渊进度: {data.stats.spiral_abyss}
普通宝箱数量: {data.stats.common_chest_number}
精致宝箱数量: {data.stats.exquisite_chest_number}
珍贵宝箱数量: {data.stats.precious_chest_number}
华丽宝箱数量: {data.stats.luxurious_chest_number}
奇馈宝箱数量: {data.stats.magic_chest_number}'''
        message = Message(
            f'[CQ:at,qq={event.get_user_id()}] {msg}')
        await genshin_data.send(message=message)
        return
    except Exception as e:
        await genshin_data.send(message=f'获取数据失败，err: {str(e)}')
