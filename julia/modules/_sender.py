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

papth = path + "thumb_image.jpg"
@register(pattern="^/rename (.*)")
async def _(event):
    if event.fwd_from:
        return
    thumb = None
    if os.path.exists(papth):
        thumb = papth
    dcevent = await event.reply(
        "Rename & Upload in process 🙄🙇‍♂️🙇‍♂️🙇‍♀️ It might take some time if file size is big",
    )
    input_str = event.pattern_match.group(1)
    if not os.path.isdir(path):
        os.makedirs(path)
    if event.reply_to_msg_id:
        start = datetime.now()
        file_name = input_str
        reply_message = await event.get_reply_message()
        c_time = time.time()
        to_download_directory = path
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloaded_file_name = await event.client.download_media(
            reply_message,
            downloaded_file_name,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, dcevent, c_time, "trying to download", file_name)
            ),
        )
        end = datetime.now()
        ms_one = (end - start).seconds
        await event.reply("ok")
        try:
            thumb = await reply_message.download_media(thumb=-1)
        except Exception:
            thumb = thumb
        if os.path.exists(downloaded_file_name):
            c_time = time.time()
            hmm = await event.client.send_file(
                event.chat_id,
                downloaded_file_name,
                force_document=False,
                supports_streaming=True,
                allow_cache=False,
                reply_to=event.message.id,
                thumb=thumb,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(
                        d, t, event, c_time, "trying to upload", downloaded_file_name
                    )
                ),
            )
            end_two = datetime.now()
            os.remove(downloaded_file_name)
            ms_two = (end_two - end).seconds
            await dcevent.edit(
                f"Downloaded file in {ms_one} seconds.\nUploaded in {ms_two} seconds."
            )
            await asyncio.sleep(2)
            await dcevent.delete()
        else:
            await dcevent.edit("File Not Found {}".format(input_str))
    else:
        await dcevent.edit(".rename file.name as reply to a Telegram media/file")
