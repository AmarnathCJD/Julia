from julia.Config import Config
from julia.events import register
from julia import CMD_HELP
from julia import tbot as borg
from julia import tbot
from julia import OWNER_ID, SUDO_USERS
from julia import TEMP_DOWNLOAD_DIRECTORY
import os
import wget
from shutil import rmtree
import cv2
import cv2 as cv
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
sedpath = "./starkgangz/"
if not os.path.isdir(sedpath):
    os.makedirs(sedpath)
from julia.Ok import upload_file

from julia.func import convert_to_image, crop_vid, runcmd, tgs_to_gif
DANISH = "58199388-5499-4c98-b052-c679b16310f9"
@register(pattern="^/nfsw")
async def hmm(event):
    if event.fwd_from:
        return
    life = DANISH
    if not event.reply_to_msg_id:
        await event.reply("Reply to any Image.")
        return
    headers = {"api-key": life}
    hmm = await event.reply("Detecting..")
    await event.get_reply_message()
    img = await convert_to_image(event, borg)
    img_file = {
        "image": open(img, "rb"),
    }
    url = "https://api.deepai.org/api/nsfw-detector"
    r = requests.post(url=url, files=img_file, headers=headers).json()
    sedcopy = r["output"]
    hmmyes = sedcopy["detections"]
    game = sedcopy["nsfw_score"]
    await hmm.delete()
    final = f"**IMG RESULT** \n**Detections :** `{hmmyes}` \n**NSFW SCORE :** `{game}`"
    await borg.send_message(event.chat_id, final)
    await hmm.delete()
    if os.path.exists(img):
        os.remove(img)

@register(pattern="^/thug")
async def iamthug(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.reply("Reply to any Image.")
        return
    hmm = await event.reply("`Converting To thug Image..`")
    await event.get_reply_message()
    img = await convert_to_image(event, borg)
    imagePath = img
    maskPath = "./resources/thuglife/mask.png"
    cascPath = "./resources/thuglife/face_regex.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.15)
    background = Image.open(imagePath)
    for (x, y, w, h) in faces:
        mask = Image.open(maskPath)
        mask = mask.resize((w, h), Image.ANTIALIAS)
        offset = (x, y)
        background.paste(mask, offset, mask=mask)
    file_name = "fridaythug.png"
    ok = sedpath + "/" + file_name
    background.save(ok, "PNG")
    await borg.send_file(event.chat_id, ok)
    await hmm.delete()
    for files in (ok, img):
        if files and os.path.exists(files):
            os.remove(files)

@register(pattern="^/(logo|blacklogo) ?(.*)")
async def yufytf(event):
    if event.fwd_from:
        return
    await event.reply("`Processing..`")
    text = event.pattern_match.group(2)
    img = Image.open('./resources/Blankmeisnub.jpg')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('resources/Streamster.ttf', 220)
    image_widthz, image_heightz = img.size
    w,h = draw.textsize(text, font=font)
    h += int(h*0.21)
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 0))
    file_name = "LogoBy@MeisNub.png"
    await event.delete()
    ok = sedpath + "/" + file_name
    img.save(ok, "PNG")
    await borg.send_file(event.chat_id, ok, caption="Made By Anie")
    if os.path.exists(ok):
        os.remove(ok)
@register(pattern="^/(slogo|starlogo) ?(.*)")
async def slogo(event):
    if event.fwd_from:
        return
    await event.edit("`Processing..`")
    text = event.pattern_match.group(2)
    img = Image.open('./resources/20201125_094030.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "white"
    shadowcolor = "black"
    font = ImageFont.truetype("./resources/Vermin Vibes V.otf", 380)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= (image_heightz-h)/2
    draw.text((x, y), text, font=font, fill="white", stroke_width=30, stroke_fill="black")
    fname2 = "LogoBy@FRIDAYOT.png"
    img.save(fname2, "png")
    await borg.send_file(event.chat_id, fname2, caption="Made By Anie")
    if os.path.exists(fname2):
            os.remove(fname2)

@register(pattern="^/(blogo|betalogo) ?(.*)")
async def slogo(event):
    if event.sender_id in SUDO_USERS:
        pass
    elif event.sender_id == OWNER_ID:
        pass
    elif event.sender_id not in SUDO_USERS:
        await event.reply("Who Are You?")
        return
    else:
        return
    await event.edit("`Processing..`")
    text = event.pattern_match.group(2)
    img = Image.open('./resources/IMG_20210215_104759_504.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "white"
    shadowcolor = "black"
    font = ImageFont.truetype("./resources/Vermin Vibes V.otf", 69)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= (image_heightz-h)/2
    draw.text((x, y), text, font=font, fill="red", stroke_width=9, stroke_fill="black")
    fname2 = "LogoBy@FRIDAYOT.png"
    img.save(fname2, "png")
    await borg.send_file(event.chat_id, fname2, caption="Made By Anie")
    if os.path.exists(fname2):
            os.remove(fname2)

@register(pattern="^/(hlogo|heppylogo) ?(.*)")
async def slogo(event):
    if event.fwd_from:
        return
    await event.edit("`Processing..`")
    text = event.pattern_match.group(2)
    img = Image.open('./resources/images (1).jpeg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "white"
    shadowcolor = "black"
    font = ImageFont.truetype("./resources/Vermin Vibes V.otf", 70)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= (image_heightz-h)/2
    draw.text((x, y), text, font=font, fill="green", stroke_width=7, stroke_fill="blue")
    fname2 = "LogoBy@FRIDAYOT.png"
    img.save(fname2, "png")
    await borg.send_file(event.chat_id, fname2, caption="Made By Anie")
    if os.path.exists(fname2):
            os.remove(fname2)
@register(pattern="^/(clogo|cyberlogo) ?(.*)")
async def slogo(event):
    if event.sender_id in SUDO_USERS:
        pass
    elif event.sender_id == OWNER_ID:
        pass
    elif event.sender_id not in SUDO_USERS:
        await event.reply("Who Are You?")
        return
    else:
        return
    await event.edit("`Processing..`")
    text = event.pattern_match.group(2)
    img = Image.open('./resources/IMG_20210215_114503_069.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "white"
    shadowcolor = "black"
    font = ImageFont.truetype("./resources/Vermin Vibes V.otf", 89)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, ((image_heightz-h)/2)-200), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2-200)
    draw.text((x, y), text, font=font, fill="orange", stroke_width=10, stroke_fill="black")
    fname2 = "LogoBy@FRIDAYOT.png"
    img.save(fname2, "png")
    await borg.send_file(event.chat_id, fname2, caption="Made By Anie")
    if os.path.exists(fname2):
            os.remove(fname2)

@register(pattern="^/(bonk|bonked) ?(.*)")
async def slogo(event):
    if event.fwd_from:
        return
    await event.edit("`Processing..`")
    text = event.pattern_match.group(2)
    img = Image.open('./resources/IMG_20210215_175652_655.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "white"
    shadowcolor = "black"
    font = ImageFont.truetype("./resources/Vermin Vibes V.otf", 380)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= (image_heightz-h)/2
    draw.text((x, y), text, font=font, fill="white", stroke_width=30, stroke_fill="black")
    fname2 = "LogoBy@FRIDAYOT.png"
    img.save(fname2, "png")
    await borg.send_file(event.chat_id, fname2, caption="Made By Anie")
    if os.path.exists(fname2):
            os.remove(fname2)
@register(pattern="^/(nlogo|nalogo) ?(.*)")
async def slogo(event):
    if event.fwd_from:
        return
    await event.edit("`Processing..`")
    text = event.pattern_match.group(2)
    img = Image.open('./resources/IMG_20210210_170521_219.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "white"
    shadowcolor = "black"
    font = ImageFont.truetype("./resources/Vermin Vibes V.otf", 380)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= (image_heightz-h)/2
    draw.text((x, y), text, font=font, fill="white", stroke_width=30, stroke_fill="black")
    fname2 = "LogoBy@FRIDAYOT.png"
    img.save(fname2, "png")
    await borg.send_file(event.chat_id, fname2, caption="Made By Anie")
    if os.path.exists(fname2):
            os.remove(fname2)
@register(pattern="^/(klogo|skayogo) ?(.*)")
async def slogo(event):
    if event.fwd_from:
        return
    await event.edit("`Processing..`")
    text = event.pattern_match.group(2)
    img = Image.open('./resources/IMG_20210215_170415_437.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "white"
    shadowcolor = "black"
    font = ImageFont.truetype("./resources/Vermin Vibes V.otf", 380)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= (image_heightz-h)/2
    draw.text((x, y), text, font=font, fill="white", stroke_width=30, stroke_fill="black")
    fname2 = "LogoBy@FRIDAYOT.png"
    img.save(fname2, "png")
    await borg.send_file(event.chat_id, fname2, caption="Made By Anie")
    if os.path.exists(fname2):
            os.remove(fname2)
