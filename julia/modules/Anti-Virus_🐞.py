import re, os
from julia import ubot, tbot
import asyncio
from telethon import events
from telethon.tl import functions
from telethon.tl import types
from pymongo import MongoClient
from julia import MONGO_DB_URI

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
    return None


@tbot.on(events.NewMessage(pattern="^/scanit$"))
async def virusscan(event):
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
    if not event.reply_to_msg_id:
       await event.reply("Reply to a file to scan it.")
       return
    c = await event.get_reply_message()
    if c.media.document is None:
       await event.reply("Thats not a file.")
       return
    chat = "@VirusTotalAV_bot"
    async with ubot.conversation(chat) as conv:
        try:
            await event.client.download_file(c, "virus")
            response = conv.wait_event(events.NewMessage(incoming=True, from_users=1356559037))
            await ubot.send_file(chat, "virus")
            response = await response
            if response.text.startswith("🧬"):
              c = await tbot.send_message(event.chat_id, response)
              # await tbot.edit_message(c, response)
            os.remove("virus")
        except Exception as e:
            os.remove("virus")
            await event.reply("Some error occurred.")
            print (e)
            return
