#Test
from julia import tbot, OWNER_ID, DEV_USERS, SUDO_USERS
from julia.events import register
import os
import asyncio
import os
import time
from datetime import datetime
from julia import TEMP_DOWNLOAD_DIRECTORY as path
from julia import TEMP_DOWNLOAD_DIRECTORY


client = tbot
thumb_image_path = "./resources/IMG_20210210_170521_219.jpg"
@register(pattern=r"^/send ?(.*)")
async def Prof(event):
    if event.sender_id == OWNER_ID:
        pass
    elif event.sender_id in DEV_USERS:
        pass
    elif event.sender_id in SUDO_USERS:
        await event.reply("You do not have permissions to run this.")
        return
    else:
        return
    thumb = thumb_image_path
    message_id = event.message.id
    input_str = event.pattern_match.group(1)
    the_plugin_file = "./julia/modules/{}.py".format(input_str)
    if os.path.exists(the_plugin_file):
     message_id = event.message.id
     await event.client.send_file(
             event.chat_id,
             the_plugin_file,
             force_document=True,
             allow_cache=False,
             thumb=thumb,
             reply_to=message_id,
         )
    else:
        await event.reply("Ekdm Bochlaik😑, File Not Found😆")

@register(pattern="^/ttf ?(.*)")
async def get(event):
    name = event.text[5:]
    m = await event.get_reply_message()
    with open(name, "w") as f:
        f.write(m.message)
    await event.delete()
    await tbot.send_file(event.chat_id, name, force_document=True)
