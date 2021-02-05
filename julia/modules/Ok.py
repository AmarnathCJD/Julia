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
        if not await can_change_info(message=event):
            return
    else:
        return
    cyber = dc()
    killer = cyber.name()
    kali = cyber.address()
    danish = cyber.credit_card_full()
    await event.reply(f"ռaʍɛ:-\n`{killer}`\n\naɖɖʀɛss:-\n`{kali}`\n\nᴄaʀɖ:-\n`{danish}`")

@register(pattern="^/gban")
async def _(event):
    if event.fwd_from:
        return
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if event.is_group:
        if await is_register_admin(event.input_chat, event.message.sender_id):
            pass
        elif event.chat_id == iid and event.sender_id == userss:
            pass
        else:
            return
    await event.reply(f"Gban Initiating...")
    await event.reply(f"Cant Remove User Is Admin")
