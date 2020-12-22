import os
from telethon import events
from telethon.utils import pack_bot_file_id
from julia.events import register
from julia import tbot, CMD_HELP
from julia.modules.sql.welcome_sql import (
    add_welcome_setting,
    get_current_welcome_settings,
    rm_welcome_setting,
    update_previous_welcome,
)
from julia.modules.sql.goodbye_sql import (
    add_goodbye_setting,
    get_current_goodbye_settings,
    rm_goodbye_setting,
    update_previous_goodbye,
)
import julia.modules.sql.rules_sql as sql
from telethon import *
from telethon.tl import *
from julia import *

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


@tbot.on(events.ChatAction())  # pylint:disable=E0602
async def _(event):
    cws = get_current_welcome_settings(event.chat_id)
    if cws:
        # logger.info(event.stringify())
        """user_added=False,
        user_joined=True,
        user_left=False,
        user_kicked=False,"""
        if event.user_joined:
            if cws.should_clean_welcome:
                try:
                    await tbot.delete_messages(  # pylint:disable=E0602
                        event.chat_id, cws.previous_welcome
                    )
                except Exception as e:  # pylint:disable=C0103,W0703
                    logger.warn(str(e))  # pylint:disable=E0602
            a_user = await event.get_user()
            chat = await event.get_chat()
            me = await tbot.get_me()

            title = chat.title if chat.title else "this chat"
            participants = await event.client.get_participants(chat)
            count = len(participants)
            mention = "[{}](tg://user?id={})".format(a_user.first_name, a_user.id)
            first = a_user.first_name
            last = a_user.last_name
            if last:
                fullname = f"{first} {last}"
            else:
                fullname = first
            username = (
                f"@{me.username}" if me.username else f"[Me](tg://user?id={me.id})"
            )
            userid = a_user.id
            current_saved_welcome_message = cws.custom_welcome_message
            mention = "[{}](tg://user?id={})".format(a_user.first_name, a_user.id)
            rules = sql.get_rules(event.chat_id)
            if rules:
             current_message = await event.reply(
                current_saved_welcome_message.format(
                    mention=mention,
                    title=title,
                    count=count,
                    first=first,
                    last=last,
                    fullname=fullname,
                    username=username,
                    userid=userid,
                ),
                file=cws.media_file_id,
                buttons=[[Button.inline('Rules ✝️', data=f'start-rules-{userid}')], [Button.inline('I am not a bot ✔️', data=f'check-bot-{userid}')]],
             )
             update_previous_welcome(event.chat_id, current_message.id)           
            else:
             current_message = await event.reply(
                current_saved_welcome_message.format(
                    mention=mention,
                    title=title,
                    count=count,
                    first=first,
                    last=last,
                    fullname=fullname,
                    username=username,
                    userid=userid,
                ),
                file=cws.media_file_id,
                buttons=[[Button.inline('Rules ✝️', data=f'start-rules-{userid}')], [Button.inline('I am not a bot ✔️', data=f'check-bot-{userid}')]],
             )
             update_previous_welcome(event.chat_id, current_message.id)

@tbot.on(events.CallbackQuery(pattern=r"start-rules-(\d+)"))
async def rm_warn(event):
    rules = sql.get_rules(event.chat_id)
    # print(rules)
    user_id = int(event.pattern_match.group(1))        
    if not event.sender_id == user_id:
       await event.answer("You haven't send that command !")
       return
    text = f"The rules for **{event.chat.title}** are:\n\n{rules}"
    try:
        await tbot.send_message(
            user_id,
            text,
            parse_mode="markdown",
            link_preview=False)
    except Exception:
        await event.answer("I can't send you the rules as you haven't started me in PM, first start me !", alert=True)

@tbot.on(events.CallbackQuery(pattern=r"check-bot-(\d+)"))
async def rm_warn(event):
    if event.via_bot_id:
       return        
    if not event.sender_id == user_id:
       await event.answer("You aren't the person whom should be verified.")
       return
    try:
        ...
    except Exception:
        await event.answer("Sorry I don't have permission to unmute you please contact some adminstrator.", alert=True)


@register(pattern="^/setwelcome")  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    msg = await event.get_reply_message()
    if msg and msg.media:
        tbot_api_file_id = pack_bot_file_id(msg.media)
        add_welcome_setting(event.chat_id, msg.message, True, 0, tbot_api_file_id)
        await event.reply("Welcome message saved. ")
    else:
        input_str = event.text.split(None, 1)
        add_welcome_setting(event.chat_id, input_str[1], True, 0, None)
        await event.reply("Welcome message saved. ")


@register(pattern="^/clearwelcome$")  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    cws = get_current_welcome_settings(event.chat_id)
    rm_welcome_setting(event.chat_id)
    await event.reply(
        "Welcome message cleared. "
        + "The previous welcome message was `{}`".format(cws.custom_welcome_message)
    )


@register(pattern="^/checkwelcome$")  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    cws = get_current_welcome_settings(event.chat_id)
    if hasattr(cws, "custom_welcome_message"):
        await event.reply(
           "This chat's welcome message is\n\n`{}`".format(cws.custom_welcome_message)
        )
    else:
        await event.reply("No welcome message found for this chat")

@tbot.on(events.ChatAction())  # pylint:disable=E0602
async def _(event):
    cws = get_current_goodbye_settings(event.chat_id)
    if cws:
        # logger.info(event.stringify())
        """user_added=False,
        user_joined=True,
        user_left=False,
        user_kicked=False,"""
        if event.user_left:
            if cws.should_clean_goodbye:
                try:
                    await tbot.delete_messages(  # pylint:disable=E0602
                        event.chat_id, cws.previous_goodbye
                    )
                except Exception as e:  # pylint:disable=C0103,W0703
                    logger.warn(str(e))  # pylint:disable=E0602
            a_user = await event.get_user()
            chat = await event.get_chat()
            me = await tbot.get_me()

            title = chat.title if chat.title else "this chat"
            participants = await event.client.get_participants(chat)
            count = len(participants)
            mention = "[{}](tg://user?id={})".format(a_user.first_name, a_user.id)
            first = a_user.first_name
            last = a_user.last_name
            if last:
                fullname = f"{first} {last}"
            else:
                fullname = first
            username = (
                f"@{me.username}" if me.username else f"[Me](tg://user?id={me.id})"
            )
            userid = a_user.id
            current_saved_goodbye_message = cws.custom_goodbye_message
            mention = "[{}](tg://user?id={})".format(a_user.first_name, a_user.id)

            current_message = await event.reply(
                current_saved_goodbye_message.format(
                    mention=mention,
                    title=title,
                    count=count,
                    first=first,
                    last=last,
                    fullname=fullname,
                    username=username,
                    userid=userid,
                ),
                file=cws.media_file_id,
            )
            update_previous_goodbye(event.chat_id, current_message.id)

@register(pattern="^/setgoodbye")  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    msg = await event.get_reply_message()
    if msg and msg.media:
        tbot_api_file_id = pack_bot_file_id(msg.media)
        add_goodbye_setting(event.chat_id, msg.message, True, 0, tbot_api_file_id)
        await event.reply("Goodbye message saved. ")
    else:
        input_str = event.text.split(None, 1)
        add_goodbye_setting(event.chat_id, input_str[1], True, 0, None)
        await event.reply("Goodbye message saved. ")


@register(pattern="^/cleargoodbye$")  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    cws = get_current_goodbye_settings(event.chat_id)
    rm_goodbye_setting(event.chat_id)
    await event.reply(
        "Goodbye message cleared. "
        + "The previous goodbye message was `{}`".format(cws.custom_goodbye_message)
    )


@register(pattern="^/checkgoodbye$")  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    cws = get_current_goodbye_settings(event.chat_id)
    if hasattr(cws, "custom_goodbye_message"):
        await event.reply(
           "This chat's goodbye message is\n\n`{}`".format(cws.custom_goodbye_message)
        )
    else:
        await event.reply("No goodbye message found for this chat")


file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
**Welcome**
 - /setwelcome <welcome message> or <reply to a text>: Saves the message as a welcome note in the chat.
 - /checkwelcome: Check whether you have a welcome note in the chat.
 - /clearwelcome: Deletes the welcome note for the current chat.

**Goodbye**
 - /setgoodbye <goodbye message> or <reply to a text>: Saves the message as a goodbye note in the chat.
 - /checkgoodbye: Check whether you have a goodbye note in the chat.
 - /cleargoodbye: Deletes the goodbye note for the current chat.

**Available variables for formatting greeting message:**
`{mention}, {title}, {count}, {first}, {last}, {fullname}, {userid}, {username}, {my_first}, {my_fullname}, {my_last}, {my_mention}, {my_username}`

**Note**: __You can't set new welcome message before deleting the previous one.__"""

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})
