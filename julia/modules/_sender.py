#Test
from julia import tbot as bot, OWNER_ID, DEV_USERS
from julia.events import register
sender = event.sender.id
@register(pattern="^/send ?(.*)")
async def _(event):
  if sender in DEV_USERS or sender in OWNER_ID:
    cmd= event.pattern_match.group(1)
    await bot.send_file(event.chat_id, cmd)
  else:
    await event.reply("Who Are You?")
    await event.delete()
