from julia.Config import Config
from julia.events import register
from julia import CMD_HELP
from julia import tbot as borg
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
from julia.Ok import upload_file as uf
from julia.func import convert_to_image, crop_vid, runcmd, tgs_to_gif

@register(pattern="^/cit")
async def hmm(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.reply("Reply to any Image.")
        return
    await event.reply("Colourzing..")
    await event.get_reply_message()
    img = await convert_to_image(event, borg)
    await event.reply("Test 2")
    net = cv2.dnn.readNetFromCaffe(
        "./julia/resources/colouregex.prototxt",
    )
    await event.reply("hmm")
    pts = np.load("./julia/resources/pts_in_hull.npy")
    class8 = net.getLayerId("class8_ab")
    conv8 = net.getLayerId("conv8_313_rh")
    pts = pts.transpose().reshape(2, 313, 1, 1)
    net.getLayer(class8).blobs = [pts.astype("float32")]
    net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]
    image = cv2.imread(img)
    scaled = image.astype("float32") / 255.0
    lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)
    resized = cv2.resize(lab, (224, 224))
    L = cv2.split(resized)[0]
    L -= 50
    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
    ab = cv2.resize(ab, (image.shape[1], image.shape[0]))
    L = cv2.split(lab)[0]
    await event.reply("hmm")
    colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)
    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
    colorized = np.clip(colorized, 0, 1)
    colorized = (255 * colorized).astype("uint8")
    file_name = "Colour.png"
    await event.reply("Hmm Okk Lodu")
    ok = sedpath + "/" + file_name
    cv2.imwrite(ok, colorized)
    await borg.send_file(event.chat_id, ok)
    await hmmu.delete()
    for files in (ok, img):
        if files and os.path.exists(files):
            os.remove(files)
