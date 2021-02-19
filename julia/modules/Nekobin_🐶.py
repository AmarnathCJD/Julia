from julia import tbot as borg
from julia.events import register 
from julia import TEMP_DOWNLOAD_DIRECTORY
import logging
import os
from datetime import datetime

import requests
from requests import exceptions, get
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)


def progress(current, total):
    logger.info(
        "Downloaded {} of {}\nCompleted {}".format(
            current, total, (current / total) * 100
        )
    )

@register(pattern="^/neko ?(.*)")
async def _(event):
    if event.fwd_from:
        return
    datetime.now()
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    input_str = event.pattern_match.group(1)
    message = "SYNTAX: `.neko <long text to include>`"
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await borg.download_media(
                previous_message,
                TEMP_DOWNLOAD_DIRECTORY,
                progress_callback=progress,
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                # message += m.decode("UTF-8") + "\r\n"
                message += m.decode("UTF-8")
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        message = "SYNTAX: `.neko <long text to include>`"
    if downloaded_file_name.endswith(".py"):
        py_file = ""
        py_file += ".py"
        data = message
        key = (
            requests.post("https://nekobin.com/api/documents", json={"content": data})
            .json()
            .get("result")
            .get("key")
        )
        url = f"https://nekobin.com/{key}{py_file}"
    else:
        data = message
        key = (
            requests.post("https://nekobin.com/api/documents", json={"content": data})
            .json()
            .get("result")
            .get("key")
        )
        url = f"https://nekobin.com/{key}"

    await event.reply(f"Pasted to Nekobin : [neko]({url})", link_preview=False)

file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /neko <text>:Type in reply to a doc or text to paste it to nekobin
"""

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})

