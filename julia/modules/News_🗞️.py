from julia import tbot, CMD_HELP
import os
import urllib.request
from typing import List
from typing import Optional
from urllib.request import urlopen
import bs4
from pymongo import MongoClient
from telethon import *
from telethon import events
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


@register(pattern="^/news$")
async def _(event):
    if event.is_group:
        return

    news_url = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"
    Client = urlopen(news_url)
    xml_page = Client.read()
    Client.close()
    soup_page = bs4.BeautifulSoup(xml_page, 'xml')
    news_list = soup_page.find_all("item")
    for news in news_list:
        title = news.title.text
        text = news.link.text
        date = news.pubDate.text
        seperator = "-" * 50
        l = "\n"
        lastisthis = title + l + text + l + date + l + seperator
        await event.reply(lastisthis)
file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /news: Returns today's American News Headlines (ONLY WORKS IN PM)
"""

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})
