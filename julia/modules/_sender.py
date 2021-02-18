#Test
from julia import tbot as bot, OWNER_ID, DEV_USERS
from julia.events import register

@register(pattern="^/send ?(.*)")
async def _(event):
  person = event.sender.id
  if person in DEV_USERS or person in OWNER_ID:
    LEGENDX= event.pattern_match.group(1)
    ok = f"julia/modules/{LEGENDX}"
    await event.reply("test")
    await bot.send_file(event.chat_id, ok)
  else:
    await event.reply("Who Are You?")
    await event.delete()
