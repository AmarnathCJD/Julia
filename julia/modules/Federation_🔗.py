import csv
import json
import os
import re
import time
import uuid
from io import BytesIO
import julia.modules.sql.feds_sql as sql
from telethon import *
from telethon.tl import *
from julia import *
from julia.events import register
from pymongo import MongoClient

# Hello bot owner, I spended for feds many hours of my life, Please don't remove this if you still respect MrYacha and peaktogoo and AyraHikari too
# Federation by MrYacha 2018-2019
# Federation rework by Mizukito Akito 2019
# Federation update v2 by Ayra Hikari 2019
# Time spended on feds = 10h by #MrYacha
# Time spended on reworking on the whole feds = 22+ hours by @peaktogoo
# Time spended on updating version to v2 = 26+ hours by @AyraHikari
# Total spended for making this features is 68+ hours
# LOGGER.info("Original federation module by MrYacha, reworked by Mizukito Akito (@peaktogoo) on Telegram.")
# ME @MissJulia_Robot has also done a lot of hard work to rewrite this in telethon so add this line as a credit. Please don't remove this if you somewhat respect me.

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

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
approved_users = db.approve

def is_user_fed_owner(fed_id, user_id):
    getsql = sql.get_fed_info(fed_id)
    if getsql is False:
        return False
    getfedowner = eval(getsql['fusers'])
    if getfedowner is None or getfedowner is False:
        return False
    getfedowner = getfedowner['owner']
    if str(user_id) == getfedowner or int(user_id) == OWNER_ID:
        return True
    else:
        return False

@register(pattern="^/newfed ?(.*)")
async def _(event):
    chat = event.chat
    user = event.sender
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch['id']
        userss = ch['user']
    if event.is_group:
        if (await is_register_admin(event.input_chat, user.id)):
            pass
        elif event.chat_id == iid and user.id == userss:
            pass
        else:
            return
    message = event.pattern_match.group(1)
    if not event.is_private:
        await event.reply(
            "Federations can only be created by privately messaging me.")
        return
    fednam = message
    if not fednam:
        await event.reply("Please write the name of the federation!")
        return
    if fednam:
        fed_id = str(uuid.uuid4())
        fed_name = fednam
        #LOGGER.info(fed_id)

        x = sql.new_fed(user.id, fed_name, fed_id)
        if not x:
            await event.reply(
                "Can't create federation!\nPlease contact @MissJuliaRobotSupport if the problem persists."
            )
            return
            
        await event.reply("**You have successfully created a new federation!**"\
                 "\nName: `{}`"\
                 "\nID: `{}`"
                 "\n\nUse the command below to join the federation:"
                 "\n`/joinfed {}`".format(fed_name, fed_id, fed_id), parse_mode="markdown")
    else:
        await event.reply("Please write down the name of the federation")

@register(pattern="^/delfed ?(.*)")
async def _(event):
 try:
    args = event.pattern_match.group(1)
    chat = event.chat
    user = event.sender
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch['id']
        userss = ch['user']
    if event.is_group:
        if (await is_register_admin(event.input_chat, user.id)):
            pass
        elif event.chat_id == iid and user.id == userss:
            pass
        else:
            return
    message = event.message.id
    if not event.is_private:
        await event.reply(
            "Federations can only be deleted by privately messaging me.")
        return
    if args:
        is_fed_id = args
        getinfo = sql.get_fed_info(is_fed_id)
        if getinfo is False:
            await event.reply("This federation does not exist.")
            return
        if int(getinfo['owner']) == int(user.id) or int(user.id) == OWNER_ID:
            fed_id = is_fed_id
        else:
            await event.reply(
                "Only federation owners can do this!")
            return
    else:
        await event.reply("What should I delete?")
        return

    if is_user_fed_owner(fed_id, user.id) is False:
        await event.reply(
            "Only federation owners can do this!")
        return
    await tbot.send_message(event.chat_id,
        "Are You sure you want to delete your federation ?\nThis cannot be reverted, you will lose your entire ban list, and '**{}**' will be permanently lost !"
        .format(getinfo['fname']),
        buttons=[[Button.inline("⚠️ Delete Federation", data="rmfed_{}".format(fed_id))], [Button.inline("Cancel", data="rmfed_cancel")]], reply_to=message)
 except Exception as e:
     print (e)

@tbot.on(events.CallbackQuery(pattern=r"rmfed(\_(.*))"))
async def delete_fed(event):
    #print("1")
    tata = event.pattern_match.group(1)
    data = tata.decode()
    fed_id = data.split('_', 1)[1]
    print (fed_id)
    if not event.is_private:
       return
    if fed_id == 'cancel':
        await event.edit("Federation deletion cancelled")
        return
    getfed = sql.get_fed_info(fed_id)
    if getfed:
        delete = sql.del_fed(fed_id)
        if delete:
            await event.edit(
                "You have removed your Federation! Now all the Groups that are connected with '**{}**' do not have a Federation."
                .format(getfed['fname']),
                parse_mode='markdown')

@register(pattern="^/renamefed ?(.*) ?(.*)")
async def _(event):
    args = event.pattern_match.group(1)
    fedid = event.pattern_match.group(2)   
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch['id']
        userss = ch['user']
    if event.is_group:
        if (await is_register_admin(event.input_chat, event.sender_id)):
            pass
        elif event.chat_id == iid and event.sender_id == userss:
            pass
        else:
            return
    if not args:
        return await event.reply("usage: `/renamefed <fed_id> <newname>`")        
    if not fedid:
        return await event.reply("usage: `/renamefed <fed_id> <newname>`")
    fed_id, newname = args, fedid
    verify_fed = sql.get_fed_info(fed_id)
    if not verify_fed:
        return await event.reply("This fed not exist in my database!")
    if is_user_fed_owner(fed_id, user.id):
        sql.rename_fed(fed_id, user.id, newname)
        await event.reply(f"Successfully renamed your fed name to {newname}!")
    else:
        await event.reply("Only federation owner can do this!")

@register(pattern="^/fedinfo$")
async def _(event):   
    chat = event.chat
    # user = event.sender
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch['id']
        userss = ch['user']
    if event.is_group:
        if (await is_register_admin(event.input_chat, event.sender_id)):
            pass
        elif event.chat_id == iid and event.sender_id == userss:
            pass
        else:
            return
    fed_id = sql.get_fed_id(chat.id)
    if not fed_id:
        await event.reply(
            "This group is not in any federation!")
        return
    info = sql.get_fed_info(fed_id)
    text = "This group is part of the following federation:"
    text += "\n{} (ID: <code>{}</code>)".format(info['fname'], fed_id)
    await event.reply(text, parse_mode="html")

@tbot.on(events.NewMessage(pattern="^/joinfed ?(.*)"))
async def _(event):   
 try:
    chat = event.chat
    user = event.sender
    args = event.pattern_match.group(1)
    if event.is_group:
        if (await is_register_admin(event.input_chat, event.sender_id)):
            pass
        else:
            return
    if event.is_private:
        await event.reply("This command is specific to the group, not to my pm !")
        return
    if not args:
       await event.reply("Where is the federation ID ?")
       return

    fed_id = sql.get_fed_id(chat.id)

    if user.id in OWNER_ID:
        pass
    else:
      try:
        async for userr in tbot.iter_participants(event.chat_id, filter=types.ChannelParticipantAdmins):
          if not isinstance(userr.participant, types.ChannelParticipantCreator):
             aid = userr.id
             if int(event.sender_id) == int(aid):
                await event.reply(
                    "Only group creators can use this command!")
                return
      except Exception as e:
         print(e)
    if fed_id:
        await event.reply("You cannot join two federations from one chat")
        return

    if len(args) >= 1:
        getfed = sql.search_fed_by_id(args)
        if getfed is False:
            await event.reply("Please enter a valid federation ID")
            return

        x = sql.chat_join_fed(args, chat.title, chat.id)
        if not x:
            await event.reply(
                "Failed to join federation! Please contact @MissJuliaRobotSupport should this problem persist!"
            )
            return

        get_fedlog = sql.get_fed_log(args)
        if get_fedlog:
            if eval(get_fedlog):
                await tbot.send_message(
                    get_fedlog,
                    "Chat *{}* has joined the federation *{}*".format(
                        chat.title, getfed['fname']),
                    parse_mode="markdown")

        await event.reply("This group has joined the federation: {}!".format(
            getfed['fname']))
 except Exception as e:
    print(e)
