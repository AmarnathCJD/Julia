#Test
from julia import tbot, OWNER_ID, DEV_USERS
from julia.events import register
client = tbot
@register(pattern=r"^/send ?(.*)")
async def Prof(event):
    input_str = event.pattern_match.group(1)
    the_plugin_file = "./julia/modules/{}.py".format(input_str)
    await event.reply("test")
    message_id = event.message.id
    await event.client.send_file(
            event.chat_id,
            the_plugin_file,
            force_document=True,
            allow_cache=False,
            reply_to=message_id,
        )
