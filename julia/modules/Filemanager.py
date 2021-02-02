#under development😂
#made by RoseLoverX
from julia import OWNER_ID
from julia.events import register
import asyncio
import os
import sys

@register(pattern="^/restart$")
async def msg(event):
    check = ups.message.sender_id
    if int(check) != int(OWNER_ID):
        return
    await event.reply(
        "Restarted, Please Wait.. "
    )
    await tbot.disconnect()
    os.execl(sys.executable, sys.executable, *sys.argv)
    quit()
