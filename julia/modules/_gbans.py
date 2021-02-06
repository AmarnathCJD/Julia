from julia import CMD_HELP
from bs4 import BeautifulSoup
import urllib
from julia import OWNER_ID
from julia import SUDO_USERS
from julia import tbot
import glob
import io
import os
import textwrap
import re
import asyncio
import urllib.request
import bs4
from bing_image_downloader import downloader
from pymongo import MongoClient
from telethon import *
from telethon.tl import functions
from telethon.tl import types
from telethon.tl.types import *
import json
import urllib.request
from julia import *
from julia.Config import Config
from julia.events import register
from telethon import events
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location
from telethon.events import ChatAction
import html
client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
approved_users = db.approve
fuk = tbot
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

async def get_full_user(event):  
    args = event.pattern_match.group(1).split(':', 1)
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.fuk.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif len(args[0]) > 0:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await event.edit("`Itz not possible without an user ID`")
            return
        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.fuk.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.fuk.get_entity(user)
        except Exception as err:
            return await event.edit("Error... Please report at @Dark_cobra_support_group", str(err))           
    return user_obj, extra

async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.fuk.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None
    return user_obj

@register(pattern="^/gban ?(.*)")
async def gben(userbot):
    dc = userbot
    sender = await dc.get_sender()
    me = await dc.fuk.get_me()
    if not sender.id == me.id:
        dark = await dc.reply("Gbanning This User !")
    else:
        dark = await dc.edit("Wait Processing.....")
    me = await userbot.fuk.get_me()
    await dark.edit(f"Trying to ban you globally..weit nd watch you nub nibba")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await userbot.get_chat()
    a = b = 0
    if userbot.is_private:
        user = userbot.chat
        reason = userbot.pattern_match.group(1)
    else:
        userbot.chat.title
    try:
        user, reason = await get_full_user(userbot)
    except:
        pass
    try:
        if not reason:
            reason = "Private"
    except:
        return await dark.edit(f"**Something W3NT Wrong 🤔**")
    if user:
        if user.id == 1221693726:
            return await dark.edit(
                f"**You nub nibba..I can't gben my creator..**"
            )
        try:
            from userbot.modules.sql_helper.gmute_sql import gmute
        except:
            pass
        try:
            await userbot.fuk(BlockRequest(user))
        except:
            pass
        testuserbot = [
            d.entity.id
            for d in await userbot.fuk.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
        for i in testuserbot:
            try:
                await userbot.fuk.edit_permissions(i, user, view_messages=False)
                a += 1
                await dark.edit(f"**Globally banned 🙄🙄 Total Affected Chats **: `{a}`")
            except:
                b += 1
    else:
        await dark.edit(f"**Reply to a user you dumbo !!**")
    try:
        if gmute(user.id) is False:
            return await dark.edit(f"**Error! User already gbanned.**")
    except:
        pass
    return await dark.edit(
        f"**Globally banned this nub nibba [{user.first_name}](tg://user?id={user.id}) Affected Chats😏 : {a} **"
    )
