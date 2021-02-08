from julia import CMD_HELP
from bs4 import BeautifulSoup
import urllib
import asyncio
from julia import tbot
import glob
import io
import os
import re
import urllib.request
from faker import Faker as an
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
bot = "Aniechat"
naam = "gey"

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

@register(pattern="^/gen ?(.*)")
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
        sysarg = event.pattern_match.group(1)
        if "" in sysarg:
        async with borg.conversation(bot) as conv:
            try:
                await conv.send_message("/gen " + sysarg)
                await asyncio.sleep(4)
                audio = await conv.get_response()
                await tbot.send_message(event.chat_id, audio.text)
                await event.delete()
            except YouBlockedUserError:
                await event.reply("Error: unblock @Carol5_bot and retry!")
