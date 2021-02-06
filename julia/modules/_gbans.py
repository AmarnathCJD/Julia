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
from PIL import Image, ImageDraw, ImageFont
import re
import asyncio
import urllib.request
from faker import Faker as dc
import bs4
import html2text
import requests
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
import sys
import traceback
client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
approved_users = db.approve
from telethon.events import ChatAction
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from telethon.tl.types import MessageEntityMentionName
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
from julia.modules.sql.global_bans_sql as sql


client = tbot

async def get_user_from_event(event):
    args = event.pattern_match.group(1).split(":", 1)
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
        extra = event.pattern_match.group(1)
    elif len(args[0]) > 0:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await event.reply(f"* Pass the user's username, id or reply!**")
            return
        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except Exception as err:
            return await event.reply("Failed \n **Error**\n", str(err))
    return user_obj, extra

async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.reply(str(err))
        return None
    return user_obj

@register(pattern="^/gban(?: |$)(.*)")
async def gspider(event):
    lazy = event
    sender = await lazy.get_sender()
    me = await lazy.client.get_me()
user_id=sender_id
    if not user_id:
        await event.reply("You don't seem to be referring to a user.")
        return
    
    if int(user_id) == OWNER_ID:
        await event.reply("There is no way I can gban this user.He is my Owner")
        return

    if int(user_id) in SUDO_USERS:
        await event.reply("I spy, with my little eye... a sudo user war! Why are you guys turning on each other?")
        return

    if user_id == bot.id:
        await event.reply("-_- So funny, lets gban myself why don't I? Nice try.")
        return

    try:
        user_chat = tbot.get_chat(user_id)
    except BadRequest as excp:
        message.reply_text(excp.message)
        return

    if user_chat.type != 'private':
        await event.reply("That's not a user!")
        return

    if sql.is_user_gbanned(user_id):
        if not reason:
            message.reply_text("This user is already gbanned; I'd change the reason, but you haven't given me one...")
            return

        old_reason = sql.update_gban_reason(user_id, user_chat.username or user_chat.first_name, reason)
        if old_reason:
            message.reply_text("This user is already gbanned, for the following reason:\n"
                               "<code>{}</code>\n"
                               "I've gone and updated it with your new reason!".format(html.escape(old_reason)),
                               parse_mode=ParseMode.HTML)
        else:
            message.reply_text("This user is already gbanned, but had no reason set; I've gone and updated it!")

        return
    
    await event.reply("⚡️ *Snaps the Banhammer* ⚡️")
    
    start_time = time.time()
    datetime_fmt = "%H:%M - %d-%m-%Y"
    current_time = datetime.utcnow().strftime(datetime_fmt)

    if chat.type != 'private':
        chat_origin = "<b>{} ({})</b>\n".format(html.escape(chat.title), chat.id)
    else:
        chat_origin = "<b>{}</b>\n".format(chat.id)
        
    banner = update.effective_user  # type: Optional[User]
    log_message = (
                 "<b>Global Ban</b>" \
                 "\n#GBANNED" \
                 "\n<b>Originated from:</b> {}" \
                 "\n<b>Status:</b> <code>Enforcing</code>" \
                 "\n<b>Sudo Admin:</b> {}" \
                 "\n<b>User:</b> {}" \
                 "\n<b>ID:</b> <code>{}</code>" \
                 "\n<b>Event Stamp:</b> {}" \
                 "\n<b>Reason:</b> {}".format(chat_origin, mention_html(banner.id, banner.first_name),
                                              mention_html(user_chat.id, user_chat.first_name),
                                                           user_chat.id, current_time, reason or "No reason given"))
                
