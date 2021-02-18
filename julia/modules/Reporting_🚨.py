import html
import os
from julia import tbot
from julia import *
from telethon import events, Button
from telethon.tl import functions
from telethon.tl import types
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import *
from telethon.errors import UserNotParticipantError
from pymongo import MongoClient
from julia import MONGO_DB_URI
from julia.events import register
from julia.modules.sql import reporting_sql as sql

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


async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):
        return isinstance(
            (
                await tbot(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerUser):
        return True


async def can_ban_users(chat, user):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            chat,
            user,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.ban_users
    )


async def can_del(chat, user):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            chat,
            user,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.delete_messages
    )


async def can_change_info(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.change_info
    )


@register(pattern="^/reports ?(.*)")
async def _(event):
    if event.is_private:
        return
    if event.is_group:
        if not await can_change_info(message=event):
            return
    chat = event.chat_id
    args = event.pattern_match.group(1)
    if args:
        if args == "on":
            sql.set_chat_setting(chat, True)
            await event.reply(
                "Turned on reporting!\nAdmins who have turned on reports will be notified when /report or @admins is called."
            )

        elif args == "off":
            sql.set_chat_setting(chat, False)
            await event.reply(
                "Turned off reporting!\nNo admins will be notified on /report or @admins"
            )
        else:
            await event.reply("Wrong option!\nEither say on or off.")
            return
    else:
        await event.reply(
            f"This group's current setting is: `{sql.chat_should_report(chat)}`",
            parse_mode="markdown",
        )


@tbot.on(events.NewMessage(pattern="^/report ?(.*)"))
async def _(event):
    if event.is_private:
        return  
    if await is_register_admin(event.input_chat, event.message.sender_id):
        return

    chat = event.chat_id
    user = event.sender
    args = event.pattern_match.group(1)

    if not sql.chat_should_report(chat):
        return

    if not event.chat.username:
        await event.reply(
            "Damn, this chat has no username so I can't markup the reported message."
        )
        return

    if event.reply_to_msg_id:
        c = await event.get_reply_message()
        reported_user = c.sender_id
        reported_user_first_name = c.sender.first_name        
        if await is_register_admin(event.input_chat, reported_user):
            await event.reply("Why are you reporting an admin ?")
            return
        
        if not args:
            await event.reply("Add a reason for reporting first.")
            return

        if user.id == reported_user:
            await event.reply("Why are you reporting yourself ?")
            return

        if user.id == BOT_ID:
            await event.reply("Why are you reporting me ?")
            return

        if reported_user == OWNER_ID:
            await event.reply("Hey, don't dare reporting my master !")
            return

        msg = (
            f"<b>⚠️ Report: </b>{html.escape(event.chat.title)}\n"
            f"<b> • Report by:</b> <p><a href='tg://user?id={user.id}'>{user.first_name}</a></p> (<code>{user.id}</code>)\n"
            f"<b> • Reported user:</b> <p><a href='tg://user?id={reported_user}'>{reported_user_first_name}</a></p> (<code>{reported_user}</code>)\n"
            f"<b> • Reason:</b> {args}"
        )
        buttons = [
            [
                Button.url(
                    "➡ Message",
                    url=f"https://t.me/{event.chat.username}/{c.id}",
                )
            ],
            [
                Button.inline(
                    "⚠ Kick",
                    data=f"report_{chat}=kick={reported_user}",
                ),
                Button.inline(
                    "⛔️ Ban",
                    data=f"report_{chat}=banned={reported_user}",
                ),
            ],
            [
                Button.inline(
                    "❎ Delete Message",
                    data=f"report_{chat}=delete={reported_user}={c.id}",
                )
            ],
        ]

        async for userr in tbot.iter_participants(
            event.chat_id, filter=ChannelParticipantsAdmins
        ):
          try:
            if userr.bot:
                pass
            else:
                await tbot.send_message(
                    userr.id, msg, buttons=buttons, parse_mode="html"
                )
                await tbot.send_message(
                    userr.id,
                    "**In case if the original message was deleted by the accused, a copy is sent to you as below 👇**",
                )
                await c.forward_to(userr.id)
          except Exception:
                pass

        try:
            await tbot.send_message(
                event.chat_id,
                f"<p><a href='tg://user?id={user.id}'>{user.first_name}</a></p> reported <p><a href='tg://user?id={reported_user}'>{reported_user_first_name}</a></p> to the admins!",
                parse_mode="html",
            )
        except Exception:
            pass

        await event.delete()

    else:
        await event.reply("Reply to a message to report it to the admins.")


@tbot.on(events.CallbackQuery(pattern=r"report_(.*)"))
async def _(event):
    queryy = event.pattern_match.group(1)
    query = queryy.decode()
    # print (query)
    splitter = query.replace("report_", "").split("=")
    # print (splitter)
    if splitter[1] == "kick":
        try:
            if not await can_ban_users(int(splitter[0]), event.sender_id):
                await event.answer("You don't have sufficient permissions.")
                return
            await tbot.kick_participant(int(splitter[0]), int(splitter[2]))
            await event.answer("✅ Succesfully kicked")

        except Exception as err:
            await event.answer("🛑 Failed to kick")
            print(err)
    elif splitter[1] == "banned":
        try:
            if not await can_ban_users(int(splitter[0]), event.sender_id):
                await event.answer("You don't have sufficient permissions.")
                return
            await tbot(
                EditBannedRequest(int(splitter[0]), int(splitter[2]), BANNED_RIGHTS)
            )
            await event.answer("✅  Succesfully Banned")

        except Exception as err:
            print(err)
            await event.answer("🛑 Failed to Ban")
    elif splitter[1] == "delete":
        try:
            if not await can_del(int(splitter[0]), event.sender_id):
                await event.answer("You don't have sufficient permissions.")
                return
            await tbot.delete_messages(int(splitter[0]), int(splitter[3]))
            await event.answer("✅ Message Deleted")

        except Exception as err:
            print(err)
            await event.answer("🛑 Failed to delete message!")


file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /report <reason>: reply to a message to report it to admins.
**NOTE:** This will not get triggered if used by admins.

**Admins only:**
 - /reports <on/off>: change report setting, or view current status.
"""

CMD_HELP.update({file_helpo: [file_helpo, __help__]})
