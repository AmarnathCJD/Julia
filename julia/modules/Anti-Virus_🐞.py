import os
from julia import tbot
from julia import CMD_HELP, VIRUS_API_KEY
from telethon import events
from telethon.tl import functions
from telethon.tl import types
from pymongo import MongoClient
from julia import MONGO_DB_URI
from julia.events import register
import cloudmersive_virus_api_client

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
approved_users = db.approve
scanfile = db.filescan

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

@register(pattern="^/autoscanit(?: |$)(.*)")
async def autoscanit(event):
    if event.fwd_from:
        return
    if event.is_private:
        return
    if MONGO_DB_URI is None:
        return
    if not await can_change_info(message=event):
        return
    input = event.pattern_match.group(1)
    chats = scanfile.find({})
    if not input:
        for c in chats:
            if event.chat_id == c["id"]:
                await event.reply(
                    "Please provide some input yes or no.\n\nCurrent setting is : **on**"
                )
                return
        await event.reply(
            "Please provide some input yes or no.\n\nCurrent setting is : **off**"
        )
        return
    if input in "on":
        if event.is_group:
            chats = scanfile.find({})
            for c in chats:
                if event.chat_id == c["id"]:
                    await event.reply(
                        "Autofilescan is already enabled for this chat.")
                    return
            scanfile.insert_one({"id": event.chat_id})
            await event.reply("I will scan all incoming files for viruses from now.")
    if input in "off":
        if event.is_group:
            chats = scanfile.find({})
            for c in chats:
                if event.chat_id == c["id"]:
                    scanfile.delete_one({"id": event.chat_id})
                    await event.reply(
                        "I will not check incoming files for viruses from now.")
                    return
        await event.reply(
                    "Autofilescan isn't enabled for this chat.")       
    
    if not input == "on" and not input == "off":
        await event.reply("I only understand by on or off")
        return
      
configuration = cloudmersive_virus_api_client.Configuration()
configuration.api_key['Apikey'] = VIRUS_API_KEY
api_instance = cloudmersive_virus_api_client.ScanApi(cloudmersive_virus_api_client.ApiClient(configuration))
allow_executables = True 
allow_invalid_files = True 
allow_scripts = True 
allow_password_protected_files = True 

@register(pattern="^/scanit$")
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
    try:
       c.media.document
    except Exception:
       await event.reply("Thats not a file.")
       return
    if c.sticker:
       await event.reply("Thats not a file.")
       return
    if c.audio:
       await event.reply("Thats not a file.")
       return
    if event.gif:
       await event.reply("Thats not a file.")
       return
    if c.photo:
       await event.reply("Thats not a file.")
       return
    if c.video:
       await event.reply("Thats not a file.")
       return   
    if c.poll:
       await event.reply("Thats not a file.")
       return
    if c.geo:
       await event.reply("Thats not a file.")
       return
    if c.game:
       await event.reply("Thats not a file.")
       return   
    try:
      virus = c.file.name
      await event.client.download_file(c, virus)
      gg= await event.reply("Scanning the file ...")
      fsize = c.file.size
      if not fsize <= 3145700: # MAX = 3MB
         await gg.edit("File size exceeds 3MB")
         return
      api_response = api_instance.scan_file_advanced(c.file.name, allow_executables=allow_executables, allow_invalid_files=allow_invalid_files, allow_scripts=allow_scripts, allow_password_protected_files=allow_password_protected_files)
      if api_response.clean_result is True:
       await gg.edit("This file is safe ✔️\nNo virus detected 🐞")
      else:
       await gg.edit("This file is Dangerous ☠️️\nVirus detected 🐞")
      os.remove(virus)
    except Exception as e:
      print(e)
      os.remove(virus)
      await gg.edit("Some error occurred.")
      return

@tbot.on(events.NewMessage(pattern=None))
async def virusscanner(event):
 chats = scanfile.find({})
 for c in chats:
  if event.chat_id == c["id"]:
    c = event.message
    try:
       c.media.document
    except Exception:
       return
    if c.sticker:
       return
    if c.audio:
       return
    if c.gif:
       return
    if c.photo:
       return
    if c.video:
       return   
    if c.poll:
       return
    if c.geo:
       return
    if c.game:
       return
    try:
      fsize = c.file.size
      if not fsize <= 3145700: # MAX = 3MB
         return
      virus = c.file.name
      await event.client.download_file(c, virus)
      gg= await event.reply("Scanning the file ...")
      api_response = api_instance.scan_file_advanced(c.file.name, allow_executables=allow_executables, allow_invalid_files=allow_invalid_files, allow_scripts=allow_scripts, allow_password_protected_files=allow_password_protected_files)
      if api_response.clean_result is True:
       await gg.edit("This file is safe ✅\nNo virus detected 🐞")
      else:
       await gg.edit("This file is Dangerous ⚠️\nVirus detected 🐞")
      os.remove(virus)
    except Exception:
      os.remove(virus)
      return
     

file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /scanit: Scan a file for virus (MAX SIZE = 3MB)
 - /autofilescan <on/off>: Automatically scans all incoming files(MAX SIZE = 3MB) in your group sent by peoples
"""

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})
