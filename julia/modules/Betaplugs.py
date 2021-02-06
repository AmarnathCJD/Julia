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
from telegraph import Telegraph
import asyncio
import shlex
from typing import Tuple
from julia import *
from julia.Config import Config
from julia.events import register
import sys
import traceback
client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
approved_users = db.approve
from telethon.errors.rpcerrorlist import YouBlockedUserError
fnt = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
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
edit_time = 1
@register(pattern="^/fake")
async def _(event):
    if event.is_group:
        pass
    else:
        return
    lol = await event.reply("Getting Fake Details...")
    cyber = dc()
    killer = cyber.name()
    kali = cyber.address()
    danish = cyber.credit_card_full()
    await asyncio.sleep(edit_time)
    await lol.edit(f"𝐍𝐚𝐦𝐞:-\n`{killer}`\n\n𝐀𝐝𝐝𝐫𝐞𝐬𝐬:-\n`{kali}`\n\n𝐂𝐚𝐫𝐝:-\n`{danish}`")

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
    
@register(pattern="^/memify (.*)")
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.reply("Usage:- memify upper text ; lower text")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.reply("Reply to a image/sticker.")
        return
    file = await tbot.download_media(
                reply_message, TEMP_DOWNLOAD_DIRECTORY
            )
    a = await event.reply("Memifying this image! (」ﾟﾛﾟ)｣ ")
    text = str(event.pattern_match.group(1)).strip()
    if len(text) < 1:
        return await a.reply("Usage:- memify upper text ; lower text")
    meme = await drawText(file, text)
    await event.client.send_file(event.chat_id, file=meme, force_document=False)
    os.remove(meme)
    await event.delete()
    await a.delete()

async def drawText(image_path, text):
    img = Image.open(image_path)
    os.remove(image_path)
    i_width, i_height = img.size
    if os.name == "nt":
        fnt = "arial.ttf"
    else:
        fnt = "/usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif-Bold.ttf"
    m_font = ImageFont.truetype(fnt, int((70 / 640) * i_width))
    if ";" in text:
        upper_text, lower_text = text.split(";")
    else:
        upper_text = text
        lower_text = ""
    draw = ImageDraw.Draw(img)
    current_h, pad = 10, 5
    if upper_text:
        for u_text in textwrap.wrap(upper_text, width=15):
            u_width, u_height = draw.textsize(u_text, font=m_font)
            draw.text(
                xy=(((i_width - u_width) / 2) - 2, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(((i_width - u_width) / 2) + 2, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=((i_width - u_width) / 2, int(((current_h / 640) * i_width)) - 2),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(((i_width - u_width) / 2), int(((current_h / 640) * i_width)) + 2),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )

            draw.text(
                xy=((i_width - u_width) / 2, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(255, 255, 255),
            )
            current_h += u_height + pad
    if lower_text:
        for l_text in textwrap.wrap(lower_text, width=15):
            u_width, u_height = draw.textsize(l_text, font=m_font)
            draw.text(
                xy=(
                    ((i_width - u_width) / 2) - 2,
                    i_height - u_height - int((20 / 640) * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(
                    ((i_width - u_width) / 2) + 2,
                    i_height - u_height - int((20 / 640) * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(
                    (i_width - u_width) / 2,
                    (i_height - u_height - int((20 / 640) * i_width)) - 2,
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(
                    (i_width - u_width) / 2,
                    (i_height - u_height - int((20 / 640) * i_width)) + 2,
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )

            draw.text(
                xy=(
                    (i_width - u_width) / 2,
                    i_height - u_height - int((20 / 640) * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(255, 255, 255),
            )
            current_h += u_height + pad
    image_name = "memify.webp"
    webp_file = os.path.join(TEMP_DOWNLOAD_DIRECTORY, image_name)
    img.save(webp_file, "webp")
    return webp_file
from apscheduler.schedulers.asyncio import AsyncIOScheduler 
from julia.modules.sql.night_mode_sql import add_nightmode, rmnightmode, get_all_chat_id, is_nightmode_indb
from telethon.tl.types import ChatBannedRights
hehes = ChatBannedRights(
    until_date=None,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    send_polls=True,
    invite_users=True,
    pin_messages=True,
    change_info=True,
)
openhehe = ChatBannedRights(
    until_date=None,
    send_messages=False,
    send_media=False,
    send_stickers=False,
    send_gifs=False,
    send_games=False,
    send_inline=False,
    send_polls=False,
    invite_users=True,
    pin_messages=True,
    change_info=True,
)

@register(pattern="^/daymode$")
async def disable_ws(event):
    if not event.is_group:
        await event.reply("You Can Only Disable Night Mode in Groups.")
        return
    if not await is_register_admin(event, bot.uid): 
        await event.reply("`You Should Be Admin To Do This!`")
        return
    if not is_nightmode_indb(str(event.chat_id)):
        await event.reply("This Chat is Has Not Enabled Night Mode.")
        return
    rmnightmode(str(event.chat_id))
    await event.reply(f"**Removed Chat {event.chat.title} With Id {event.chat_id} From Database. This Group Will Be No Longer Closed On 12Am(IST) And Will Opened On 06Am(IST)**")

@register(pattern="^/nightmode$")
async def job_close():
    ws_chats = get_all_chat_id()
    if len(ws_chats) == 0:
        return
    for warner in ws_chats:
        try:
            await event.send_message(
              int(warner.chat_id), "`12:00 Am, Group Is Closing Till 6 Am. Night Mode Started !` \n**Powered By @FRidayOT**"
            )
            await event(
            functions.messages.EditChatDefaultBannedRightsRequest(
                peer=int(warner.chat_id), banned_rights=hehes
            )
            )
            if Config.CLEAN_GROUPS:
                async for user in friday.iter_participants(int(warner.chat_id)):
                    if user.deleted:
                        await friday.edit_permissions(int(warner.chat_id), user.id, view_messages=False)
        except Exception as e:
            logger.info(f"Unable To Open Group {warner} - {e}")

scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(job_close, trigger="cron", hours=23, minutes=5)
scheduler.start()


async def job_open():
    ws_chats = get_all_chat_id()
    if len(ws_chats) == 0:
        return
    for warner in ws_chats:
        try:
            await event.send_message(
              int(warner.chat_id), "`06:00 Am, Group Is Opening.`\n**Powered By @FRidayOT**"
            )
            await friday(
            functions.messages.EditChatDefaultBannedRightsRequest(
                peer=int(warner.chat_id), banned_rights=openhehe
            )
        )
        except Exception as e:
            logger.info(f"Unable To Open Group {warner.chat_id} - {e}")

# Run everyday at 06
scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(job_open, trigger="cron", hour=6, minute=10)
scheduler.start()
