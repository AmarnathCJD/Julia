import re, os
from julia import ubot, tbot, CMD_HELP
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
    #sender_id = event.message
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
    try:
       c.media.document
    except:
       await event.reply("Thats not a file.")
       return
    o = await ubot.get_entity("@VirusTotalAV_bot")
    async with ubot.conversation(o) as y:
     try:
      virus = c.file.name
      await event.client.download_file(c, virus)
      await y.send_file(file=virus)
      response = await y.wait_event(events.MessageEdited(from_users=o.id))
      response = await y.wait_event(events.MessageEdited(from_users=o.id))
      response = await y.wait_event(events.MessageEdited(from_users=o.id))
      await tbot.send_message(event.chat_id, response.message, reply_to=sender_id)
     except Exception as e:
      os.remove(virus)
      await event.reply("Some error occurred.")
      print (e)
      return


file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
- /scanit: Scan a file for virus with the help of virustotal.com
"""

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})
