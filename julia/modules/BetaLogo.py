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

k = ("22", "12", "15", "30", "35", "20", "26")
st = random.choice(k)

n = ("black", "green", "red", "blue", "magenta", "pink", "lightgreen", "brickred", "cherryred", "brown", "violet", "orange", "yellow", "gold", "silver")
col = random.choice(n)

@tbot.on(events.NewMessage(pattern="^/logu (.*)"))
async def slogo(event):
    if event.fwd_from:
        return
    quew = event.pattern_match.group(1)
    if "|" in quew:
        iid, reasonn = quew.split("|")
    cid = iid.strip()
    reason = reasonn.strip()
    await event.reply("`Processing..`")
    text = cid
    hmm = "IMG_20210219_203337_228.jpg"
    img = Image.open(f'./resources/{hmm}')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "white"
    shadowcolor = "black"
    font = ImageFont.truetype("./resources/Blacksword.otf", 125)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+6)
    n = ("black", "green", "red", "blue", "magenta", "pink", "lightgreen", "brickred", "cherryred", "brown", "violet", "orange", "yellow", "gold", "silver")
    col = random.choice(n)
    draw.text((x, y), text, font=font, fill=f"{reason}", stroke_width=8, stroke_fill=f"{col}")
    fname2 = "LogoBy@FRIDAYOT.png"
    img.save(fname2, "png")
    await borg.send_file(event.chat_id, fname2, caption="Made By Anie")
    if os.path.exists(fname2):
            os.remove(fname2)
