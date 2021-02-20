from julia.Config import Config
from julia.events import register
from julia import CMD_HELP
from julia import tbot as borg
from julia import TEMP_DOWNLOAD_DIRECTORY
import os
from telethon import events
import random
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

@tbot.on(events.NewMessage(pattern="^/logo (.*)"))
async def slogo(event):
    if event.sender_id in SUDO_USERS:
        pass
    elif event.sender_id == OWNER_ID:
        pass
    elif event.sender_id not in SUDO_USERS:
        await event.reply("Sed")
        return
    else:
        return
    text = event.pattern_match.group(1)
    img = Image.open('./julia/resources/IMG_20210220_225112_240.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "white"
    shadowcolor = "black"
    font = ImageFont.truetype("./julia/resources/fonts/Thicxer-8MerB.ttf", 140)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="red", stroke_width=8, stroke_fill="black")
    fname2 = "LogoBy@FRIDAYOT.png"
    img.save(fname2, "png")
    await borg.send_file(event.chat_id, fname2, caption="Made By Anie")
    if os.path.exists(fname2):
            os.remove(fname2)
