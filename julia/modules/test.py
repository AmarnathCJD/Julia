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
from julia.Config import Config

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
        await event.reply("Processing ...wait")
        await asyncio.sleep(3)
        if Config.GOOGLE_CHROME_BIN is None:
        await event.reply("need to install Google Chrome. Module Stopping.")
        else:
        await event.reply("Chrome Configured")

