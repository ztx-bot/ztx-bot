from nonebot import on_command

from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent


get_all_members = on_command('get_all_members', rule=to_me())


@get_all_members.handle()
async def get_all_members_handle(bot: Bot, event: GroupMessageEvent):
    members = await bot.get_group_member_list(group_id=event.group_id)
    msg = ""
    for m in members:
        msg += f'{m["nickname"]} {m["user_id"]}\n'
        if len(msg) > 256:
            msg += '...'
            break
    await get_all_members.send(message=msg)
