from random import randint
from PIL import ImageEnhance, ImageOps
from random import uniform
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import asyncio
import io
import os
import random
import re
import string
import nltk
from PIL import Image
from zalgo_text import zalgo
from julia.events import register
import json
import subprocess
import textwrap
import urllib.request
from random import randrange
from typing import List
from typing import Optional
import emoji
from cowpy import cow
from fontTools.ttLib import TTFont
from PIL import ImageDraw
from PIL import ImageFont
from pymongo import MongoClient
from telethon import *
from telethon.tl import functions
from telethon.tl.types import *
from julia import *

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")

WIDE_MAP = {i: i + 0xFEE0 for i in range(0x21, 0x7F)}
WIDE_MAP[0x20] = 0x3000


client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
approved_users = db.approve


async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):

        return isinstance(
            (await
             tbot(functions.channels.GetParticipantRequest(chat,
                                                           user))).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerChat):

        ui = await tbot.get_peer_id(user)
        ps = (await tbot(functions.messages.GetFullChatRequest(chat.chat_id)
                         )).full_chat.participants.participants
        return isinstance(
            next((p for p in ps if p.user_id == ui), None),
            (types.ChatParticipantAdmin, types.ChatParticipantCreator),
        )
    return None

@register(pattern="^/test$")
async def msg(event):
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if event.is_group:
        if (await is_register_admin(event.input_chat, event.message.sender_id)):
            pass
        elif event.chat_id == iid and event.sender_id == userss:
            pass
        else:
            return
async def coder_print(event):
	a = await event.client.download_media(await event.get_reply_message(), Var.TEMP_DOWNLOAD_DIRECTORY)
	s = open(a, 'r')
	c = s.read()
	s.close()
	pygments.highlight(f"{c}", Python3Lexer(), ImageFormatter(font_name="DejaVu Sans Mono", line_numbers=True), "out.png")
	res = await event.client.send_message(event.chat_id, "**Pasting this code on my page pls weitðŸ¤“...**", reply_to=event.reply_to_msg_id)
	await event.client.send_file(event.chat_id, "out.png", force_document=True, reply_to=event.reply_to_msg_id)
	await event.client.send_file(event.chat_id, "out.png", force_document=False, reply_to=event.reply_to_msg_id)
	await res.delete()
	await event.delete()
	os.remove(a)
	os.remove('out.png')
