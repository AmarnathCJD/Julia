#Test
from julia import tbot as bot, OWNER_ID, DEV_USERS
from julia.events import register

@register(pattern="^/send ?(.*)")
async def _(event):
  sender = event.sender.id
  if sender in DEV_USERS or sender in OWNER_ID:
    LEGENDX= event.pattern_match.group(1)
    await bot.send_file(event.chat_id, LEGENDX)
  else:
    await event.reply("Who Are You?")
    await event.delete()
