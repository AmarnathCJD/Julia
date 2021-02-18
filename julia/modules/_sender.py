#MADE BY LEGENDX22
#CREDITS TEAMLEGEND AND ROSELOVERX

from julia import tbot as bot, OWNER_ID, SUDO_USERS
from julia.events import register
PROBOY = event.sender.id
@register(pattern="^/send ?(.*)")
async def LEGENDX(event):
  if PROBOY in SUDO_USERS or PROBOY in OWNER_ID:
    LEGENDX= event.pattern_match.group(1)
    await bot.send_file(event.chat_id, LEGENDX)
  else:
    await event.reply("JA NA LODE")
    await event.delete()
