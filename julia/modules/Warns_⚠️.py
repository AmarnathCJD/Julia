from julia import CMD_HELP, tbot
import html
import os
from telethon import *
from telethon.tl import *
from julia.events import register
import julia.modules.sql.warns_sql as sql
from telethon.tl.types import (ChatBannedRights)
from telethon.tl import functions
from telethon.tl import types
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import *


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


@tbot.on(events.NewMessage(pattern="^/warn"))
async def _(event):
    if event.fwd_from:
        return
    if event.is_private:
        return
    if event.is_group:
        if await is_register_admin(event.input_chat, event.message.sender_id):
            pass
        else:
            return
    warn_getter = event.text
    warn_reason = warn_getter.split(" ", maxsplit=1)[1]
    if not warn_reason:
        await event.reply("Please provide a reason for warning.")
        return
    reply_message = await event.get_reply_message()
    if not await is_register_admin(event.input_chat, reply_message.sender_id):
            pass
    else:
           await event.reply("I am not gonna warn an admin")
           return
    limit, soft_warn = sql.get_warn_setting(event.chat_id)
    num_warns, reasons = sql.warn_user(
        reply_message.sender_id, event.chat_id, warn_reason)
    if num_warns >= limit:
        sql.reset_warns(reply_message.sender_id, event.chat_id)
        if soft_warn:
            await tbot.kick_participant(event.chat_id, reply_message.sender_id)
            reply = "{} warnings, <u><a href='tg://user?id={}'>user</a></u> has been kicked!".format(
                limit, reply_message.sender_id)
            await event.reply(reply, parse_mode="html")
            return
        BANNED_RIGHTS = ChatBannedRights(
           until_date=None,
           view_messages=True,
           send_messages=True,
           send_media=True,
           send_stickers=True,
           send_gifs=True,
           send_games=True,
           send_inline=True,
           embed_links=True,
        )
        await tbot(EditBannedRequest(event.chat_id, reply_message.sender_id, BANNED_RIGHTS))      
        reply = "{} warnings, <u><a href='tg://user?id={}'>user</a></u> has been banned!".format(
            limit, reply_message.sender_id)
        await event.reply(reply, parse_mode="html")
        return
    else:
        reply = "<u><a href='tg://user?id={}'>user</a></u> has {}/{} warnings... watch out!".format(
            reply_message.sender_id, num_warns, limit)
        if warn_reason:
            reply += "\nReason: {}".format(html.escape(warn_reason))
    
    await event.reply(reply, buttons=[[Button.inline('Remove Warn ✖️', data=f"rm_warn-{reply_message.sender_id}")]], parse_mode="html")

@tbot.on(events.CallbackQuery(pattern=r"rm_warn-(\d+)"))
async def rm_warn(event):
   try:
    if event.is_group:
        if await is_register_admin(event.input_chat, event.sender_id):
            pass
        else:
            await event.answer("You need to be an admin to do this", alert=False)
        sender = await event.get_sender()
        sid= sender.id
        user_id = int(event.pattern_match.group(1))
        result = sql.get_warns(user_id, event.chat_id)
        if not result and result[0] != 0:
            await event.answer("This user hasn't got any warnings!", alert=False)
            return
        sql.remove_warn(user_id, event.chat_id)
        await event.edit(f"Warn removed by <u><a href='tg://user?id={sid}'>user</a></u> ", parse_mode="html")
    else:
        return
   except:
      await event.answer("Sorry the button link has expired, pls use /removelastwarn to manually remove warns", alert=True)
       
@register(pattern="^/getwarns$")
async def _(event):
    if event.fwd_from:
        return
    if event.is_private:
        return
    if event.is_group:
        if await is_register_admin(event.input_chat, event.message.sender_id):
            pass

        else:
            return
    reply_message = await event.get_reply_message()
    if not await is_register_admin(event.input_chat, reply_message.sender_id):
            pass
    else:
           await event.reply("I am not gonna get warns of an admin")
           return
    result = sql.get_warns(reply_message.sender_id, event.chat_id)
    if result and result[0] != 0:
        num_warns, reasons = result
        limit, soft_warn = sql.get_warn_setting(event.chat_id)
        if reasons:
            text = "This user has {}/{} warnings, for the following reasons:".format(
                num_warns, limit)
            text += "\r\n"
            text += reasons
            await event.reply(text)
        else:
            await event.reply("This user has {} / {} warning, but no reasons for any of them.".format(num_warns, limit))
    else:
        await event.reply("This user hasn't got any warnings!")


@register(pattern="^/removelastwarn$")
async def _(event):
    if event.fwd_from:
        return
    if event.is_private:
        return
    if event.is_group:
        if await is_register_admin(event.input_chat, event.message.sender_id):
            pass
        else:
            return
    reply_message = await event.get_reply_message()
    if not await is_register_admin(event.input_chat, reply_message.sender_id):
            pass
    else:
           await event.reply("I am not gonna remove warn of an admin")
           return
    result = sql.get_warns(reply_message.sender_id, event.chat_id)
    if not result and result[0] != 0:
        await event.reply("This user hasn't got any warnings!")
        return
    sql.remove_warn(reply_message.sender_id, event.chat_id)
    await event.reply("Removed last warn of that user.")

@register(pattern="^/resetwarns$")
async def _(event):
    if event.fwd_from:
        return
    if event.is_private:
        return
    if event.is_group:
        if await is_register_admin(event.input_chat, event.message.sender_id):
            pass

        else:
            return
    reply_message = await event.get_reply_message()
    if not await is_register_admin(event.input_chat, reply_message.sender_id):
            pass
    else:
           await event.reply("I am not gonna reset warn of an admin")
           return
    sql.reset_warns(reply_message.sender_id, event.chat_id)
    await event.reply("Warns for this user have been reset!")
file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /warn: warn a user
 - /removelastwarn: remove the last warn that a user has received
 - /getwarns: list the warns that a user has received
 - /resetwarns: reset all warns that a user has received
 - /warnmode <kick/ban>: set the warn mode for the chat
"""

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})
