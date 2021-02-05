from julia import CMD_HELP
from bs4 import BeautifulSoup
import urllib
from julia import tbot
import glob
import io
import os
import re
import urllib.request
from faker import Faker as dc
import bs4
import html2text
import requests
from bing_image_downloader import downloader
from PIL import Image
from pymongo import MongoClient
from telethon import *
from telethon.tl import functions
from telethon.tl import types
from telethon.tl.types import *
import json
import urllib.request
from julia import *

from julia.events import register

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
approved_users = db.approve
from telethon.errors.rpcerrorlist import YouBlockedUserError

async def can_change_info(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (isinstance(
        p, types.ChannelParticipantAdmin) and p.admin_rights.change_info)



@register(pattern="^/fake")
async def _(event):
    if event.is_group:
        pass
    else:
        return
    cyber = dc()
    killer = cyber.name()
    kali = cyber.address()
    danish = cyber.credit_card_full()
    await event.reply(f"ռaʍɛ:-\n`{killer}`\n\naɖɖʀɛss:-\n`{kali}`\n\nᴄaʀɖ:-\n`{danish}`")

@register(pattern="^/iplookup (.*)")
async def _(event):
    if event.is_group:
        pass
    else:
        return
    input_str = event.pattern_match.group(1)

    adress = input_str

    token = "19e7f2b6fe27deb566140aae134dec6b"

    api = "http://api.ipstack.com/" + adress + "?access_key=" + token + "&format=1"

    result = urllib.request.urlopen(api).read()
    result = result.decode()

    result = json.loads(result)
    a = result["type"]
    b = result["country_code"]
    c = result["region_name"]
    d = result["city"]
    e = result["zip"]
    f = result["latitude"]
    g = result["longitude"]
    await event.reply(
        f"<b><u>INFORMATION GATHERED SUCCESSFULLY</b></u>\n<b>IP:-</b><code>{input_str}</code>\n\n<b>Ip type :-</b><code>{a}</code>\n<b>Country code:- </b> <code>{b}</code>\n<b>State name :-</b><code>{c}</code>\n<b>City name :- </b><code>{d}</code>\n<b>zip :-</b><code>{e}</code>\n<b>Latitude:- </b> <code>{f}</code>\n<b>Longitude :- </b><code>{g}</code>\n",
        parse_mode="HTML",
    )
    
