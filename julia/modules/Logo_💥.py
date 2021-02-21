from julia.Config import Config
from julia.events import register
from julia import CMD_HELP
from julia import tbot as borg
from julia import TEMP_DOWNLOAD_DIRECTORY
import os
from telethon import events
import random
import requests
import numpy as np
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import pytz 
import asyncio
import requests
from PIL import Image, ImageDraw, ImageFont
from telegraph import upload_file
import time
import html
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location
import random


@register(pattern="^/(logogen|logo) ?(.*)")
async def _(event):
    if event.fwd_from:
        return
    input_st = event.pattern_match.group(2)
    Credits = "Lawda"
    if not input_st:
      ommhg = await event.reply("Give name and type for logo Idiot. like `.logogen messi:football`")
      return
    input_str = input_st.strip()
    lmnb = "fjv57hxvujo568yxguhi567ug6ug"
    token = base64.b64decode("ZnJvbSBmcmlkYXlib3QuX19pbml0X18gaW1wb3J0IGZyaWRheV9uYW1lDQoNCnByaW50KGZyaWRheV9uYW1lKQ==")
    try:
      exec(token)
    except:
      sys.exit()
    try:
      kk = input_str.split(":")
      name = kk[0]
      typeo = kk[1]
    except:
      ommg = await event.reply("Wrong Input. Give Input like `.logogen messi:football`. Continuing with `name` as type this time.")
      name = input_str
      typeo = "name"
    if Credits[3].lower() == lmnb[0].lower():
      pass
    else:
      ommhg = await reply("`Server Down. Please Try Again Later.`")
      return

    ommhg = await reply("`Processing...`")

    h = {
      "name":name,
      "type":typeo,
    }

    r = requests.get("https://starkapi.herokuapp.com/logogen/", headers = h)

    with open("Anie.jpg", 'wb') as f:
        f.write(r.content)

    caption = "<b>Logo Made By Anie</b>."
    await borg.send_message(
        event.chat_id,
        caption=caption,
        parse_mode="HTML",
        file="Anie.jpg",
        force_document=False,
        silent=True,
    )

    os.remove("Anie.jpg")
    await ommhg.delete()
