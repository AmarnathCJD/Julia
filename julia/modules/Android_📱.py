from julia import CMD_HELP
import os
from julia import tbot
import json
import re

import rapidjson as json
from bs4 import BeautifulSoup
from requests import get
from telethon import types
from telethon.tl import functions
from julia.events import register
from pymongo import MongoClient
from julia import MONGO_DB_URI

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
approved_users = db.approve

GITHUB = "https://github.com"


async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):

        return isinstance(
            (
                await tbot(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerChat):

        ui = await tbot.get_peer_id(user)
        ps = (
            await tbot(functions.messages.GetFullChatRequest(chat.chat_id))
        ).full_chat.participants.participants
        return isinstance(
            next((p for p in ps if p.user_id == ui), None),
            (types.ChatParticipantAdmin, types.ChatParticipantCreator),
        )
    return None


@register(pattern=r"^/device(?: |$)(\S*)")
async def device_info(request):
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if request.is_group:
        if (await is_register_admin(request.input_chat, request.message.sender_id)):
            pass
        elif request.chat_id == iid and request.sender_id == userss:
            pass
        else:
            return
    """ get android device basic info from its codename """
    textx = await request.get_reply_message()
    codename = request.pattern_match.group(1)
    if codename:
        pass
    elif textx:
        codename = textx.text
    else:
        await request.reply("`Usage: /device <codename> / <model>`")
        return
    data = json.loads(
        get(
            "https://raw.githubusercontent.com/androidtrackers/"
            "certified-android-devices/master/by_device.json"
        ).text
    )
    results = data.get(codename)
    if results:
        reply = f"**Search results for {codename}**:\n\n"
        for item in results:
            reply += (
                f"**Brand**: {item['brand']}\n"
                f"**Name**: {item['name']}\n"
                f"**Model**: {item['model']}\n\n"
            )
    else:
        reply = f"`Couldn't find info about {codename}!`\n"
    await request.reply(reply)


@register(pattern=r"^/codename(?: |)([\S]*)(?: |)([\s\S]*)")
async def codename_info(request):
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if request.is_group:
        if (await is_register_admin(request.input_chat, request.message.sender_id)):
            pass
        elif request.chat_id == iid and request.sender_id == userss:
            pass
        else:
            return
    """ search for android codename """
    textx = await request.get_reply_message()
    brand = request.pattern_match.group(1).lower()
    device = request.pattern_match.group(2).lower()

    if brand and device:
        pass
    elif textx:
        brand = textx.text.split(" ")[0]
        device = " ".join(textx.text.split(" ")[1:])
    else:
        await request.reply("`Usage: /codename <brand> <device>`")
        return

    data = json.loads(
        get(
            "https://raw.githubusercontent.com/androidtrackers/"
            "certified-android-devices/master/by_brand.json"
        ).text
    )
    devices_lower = {k.lower(): v for k, v in data.items()}
    devices = devices_lower.get(brand)
    results = [
        i
        for i in devices
        if i["name"].lower() == device.lower() or i["model"].lower() == device.lower()
    ]
    if results:
        reply = f"**Search results for {brand} {device}**:\n\n"
        if len(results) > 8:
            results = results[:8]
        for item in results:
            reply += (
                f"**Device**: {item['device']}\n"
                f"**Name**: {item['name']}\n"
                f"**Model**: {item['model']}\n\n"
            )
    else:
        reply = f"`Couldn't find {device} codename!`\n"
    await request.reply(reply)


@register(pattern=r"^/specs(?: |)([\S]*)(?: |)([\s\S]*)")
async def devices_specifications(request):
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if request.is_group:
        if (await is_register_admin(request.input_chat, request.message.sender_id)):
            pass
        elif request.chat_id == iid and request.sender_id == userss:
            pass
        else:
            return
    """ Mobile devices specifications """
    textx = await request.get_reply_message()
    brand = request.pattern_match.group(1).lower()
    device = request.pattern_match.group(2).lower()
    if brand and device:
        pass
    elif textx:
        brand = textx.text.split(" ")[0]
        device = " ".join(textx.text.split(" ")[1:])
    else:
        await request.reply("`Usage: /specs <brand> <device>`")
        return
    all_brands = (
        BeautifulSoup(
            get("https://www.devicespecifications.com/en/brand-more").content,
            "lxml") .find(
            "div",
            {
                "class": "brand-listing-container-news"}) .findAll("a"))
    brand_page_url = None
    try:
        brand_page_url = [
            i["href"] for i in all_brands if brand == i.text.strip().lower()
        ][0]
    except IndexError:
        await request.reply(f"`{brand} is unknown brand!`")
    devices = BeautifulSoup(get(brand_page_url).content, "lxml").findAll(
        "div", {"class": "model-listing-container-80"}
    )
    device_page_url = None
    try:
        device_page_url = [
            i.a["href"]
            for i in BeautifulSoup(str(devices), "lxml").findAll("h3")
            if device in i.text.strip().lower()
        ]
    except IndexError:
        await request.reply(f"`can't find {device}!`")
    if len(device_page_url) > 2:
        device_page_url = device_page_url[:2]
    reply = ""
    for url in device_page_url:
        info = BeautifulSoup(get(url).content, "lxml")
        reply = "\n" + info.title.text.split("-")[0].strip() + "\n"
        info = info.find("div", {"id": "model-brief-specifications"})
        specifications = re.findall(r"<b>.*?<br/>", str(info))
        for item in specifications:
            title = re.findall(r"<b>(.*?)</b>", item)[0].strip()
            data = (
                re.findall(r"</b>: (.*?)<br/>", item)[0]
                .replace("<b>", "")
                .replace("</b>", "")
                .strip()
            )
            reply += f"**{title}**: {data}\n"
    await request.reply(reply)


@register(pattern=r"^/twrp(?: |$)(\S*)")
async def twrp(request):
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if request.is_group:
        if (await is_register_admin(request.input_chat, request.message.sender_id)):
            pass
        elif request.chat_id == iid and request.sender_id == userss:
            pass
        else:
            return

    """ get android device twrp """
    textx = await request.get_reply_message()
    device = request.pattern_match.group(1)
    if device:
        pass
    elif textx:
        device = textx.text.split(" ")[0]
    else:
        await request.reply("`Usage: /twrp <codename>`")
        return
    url = get(f"https://dl.twrp.me/{device}/")
    if url.status_code == 404:
        reply = f"`Couldn't find twrp downloads for {device}!`\n"
        await request.reply(reply)
        return
    page = BeautifulSoup(url.content, "lxml")
    download = page.find("table").find("tr").find("a")
    dl_link = f"https://dl.twrp.me{download['href']}"
    dl_file = download.text
    size = page.find("span", {"class": "filesize"}).text
    date = page.find("em").text.strip()
    reply = (
        f"**Latest TWRP for {device}:**\n"
        f"[{dl_file}]({dl_link}) - __{size}__\n"
        f"**Updated:** __{date}__\n"
    )
    await request.reply(reply)
file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /device <codename>: Get info about an Android device
 - /codename <brand> <device>: Search for Android device codename
 - /specs <brand> <device>: Get device specifications info
 - /twrp <codename>: Get the latest TWRP download for an Android device
"""

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})
