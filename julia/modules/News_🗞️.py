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


@register(pattern="^/news (.*) (.*)")
async def _(event):
    sender = event.sender_id
    country = event.pattern_match.group(1)
    lang = event.pattern_match.group(2)
    index = 0
    chatid = event.chat_id
    msg = await tbot.send_message(chatid, "Loading ...")
    msgid = msg.id
    await tbot.send_message("Click on the below button to read the latest news headlines 👇", buttons=[[Button.inline('▶️', data=f'news-{sender}|{country}|{lang}|{index}|{chatid}|{msgid}')]])

@tbot.on(events.CallbackQuery(pattern=r"news(\-(.*))"))
async def paginate_news(event):
    tata = event.pattern_match.group(1)
    data = tata.decode()
    meta = data.split('-', 1)[1]
    #print(meta)
    if "|" in meta:
        sender, country, lang, index, chatid, msgid = meta.split("|")
    sender = int(sender.strip())
    if not event.sender_id == sender:
       await event.answer("You haven't send that command !")
       return
    country = country.strip()
    lang = lang.strip()
    index = index.strip()
    num = int(index)
    chatid = int(chatid.strip())
    msgid = int(msgid.strip())
    news_url = f"https://news.google.com/rss?hl={lang}-{country}&gl={country}&ceid={country}:{lang}"
    Client = urlopen(news_url)
    xml_page = Client.read()
    Client.close()
    soup_page = bs4.BeautifulSoup(xml_page, 'xml')
    news_list = soup_page.find_all("item")
    header = f"**#{num} **"
    title = news_list[f"{num}"].title.text
    text = news_list[f"{num}"].link.text
    date = news_list[f"{num}"].pubDate.text
    lastisthis = f"{header}[{title}]({text})"+"\n\n"+ f"{date}"
    await tbot.edit_message(chatid, msgid, lastisthis, link_preview=False) # buttons=[[Button.inline('▶️', data=f'news-en-{sender}')]])

file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /news <country code> <LanguageCode>: Returns today's American News Headlines (ONLY WORKS IN PM)
**Example:**
 - /news US en: This will return news for US in english language.
"""

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})
