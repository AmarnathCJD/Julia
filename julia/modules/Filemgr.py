#made by RoseLoverX Jo Kang Kiya Wo Mera beta Ho
from PIL import ImageEnhance, ImageOps
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import re
import string
import nltk
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
from fontTools.ttLib import TTFont
from pymongo import MongoClient
from telethon import *
from telethon.tl import functions
from telethon.tl.types import *
from julia import *
from julia.Config import Config
import traceback
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location
WIDE_MAP = {i: i + 0xFEE0 for i in range(0x21, 0x7F)}
WIDE_MAP[0x20] = 0x3000
from PIL import Image
from telegraph import Telegraph, exceptions, upload_file
import requests
client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
approved_users = db.approve
import io
import os
import os.path
import time
from os.path import exists, isdir
import sys
import asyncio
from datetime import datetime
from pathlib import Path
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

@register(pattern="^/restart$")
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
    await asyncio.sleep(2)
    await event.reply("Restarting  ▰▰▰▱▱▱▱▱▱▱...")
    await asyncio.sleep(2)
    await event.reply("Restarting  ▰▰▰▰▰▰▰▰▱▱..")
    await asyncio.sleep(2)
    await event.reply(
        "Restarted,wait... `.ping` me or type `.help`  to check if your anie userbot is online/alive "
    )
    await tbot.disconnect()
    os.execl(sys.executable, sys.executable, *sys.argv)
    quit()
