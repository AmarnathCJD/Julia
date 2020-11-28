from julia import tbot, CMD_HELP
import os
import subprocess
import urllib.request
from typing import List
from typing import Optional
import telegraph
from pymongo import MongoClient
from telegraph import Telegraph
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
    return False


telegraph = Telegraph()
telegraph.create_account(short_name="Julia")


@register(pattern="^/torrent (.*)")
async def tor_search(event):
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
    str = event.pattern_match.group(1)
    let = f'"{str}"'
    jit = subprocess.check_output(["we-get", "-s", let, "-t", "all", "-J"])
    proc = jit.decode()
    sit = proc.replace("{", "")
    pit = sit.replace("}", "")
    op = pit.replace(",", "")
    seta = f"Magnets for {str} are below:"
    response = telegraph.create_page(seta, html_content=op)
    await event.reply(
        "Magnet Links for {}:\n\nhttps://telegra.ph/{}".format(str, response["path"]),
        link_preview=False,
    )
file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /torrent <text>: Search for torrent links
If you are still messed up send `/helptorrent` in pm for the tutorial !
"""
CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})
