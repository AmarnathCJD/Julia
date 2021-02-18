#Test
from julia import tbot, OWNER_ID, DEV_USERS
from julia.events import register
client = tbot
@register(pattern="^/send ?(.*)")
async def _(event):
  person = event.sender.id
  if person in DEV_USERS or person in OWNER_ID:
    input_str = event.pattern_match.group(1)
    the_plugin_file = "./julia/modules/{}.py".format(input_str)
    await event.reply("test")
    await event.client.send_file(
            event.chat_id,
            the_plugin_file,
            force_document=True,
            allow_cache=False,
        )
  else:
    await event.reply("Who Are You?")
    await event.delete()
