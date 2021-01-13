import csv
import json
import os
import re
import time
import uuid
from io import BytesIO
import julia.modules.sql.feds_sql as sql
from telethon import *
from julia import *
from julia.events import register

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

@register(pattern="^/newfed ?(.*)")
async def _(event):
    chat = event.chat
    user = event.sender
    message = event.message
    if event.is_private:
        await event.reply(
            "Federations can only be created by privately messaging me.")
        return
    if len(message.text) == 1:
        await event.reply("Please write the name of the federation!")
        return
    fednam = message.text.split(None, 1)[1]
    if not fednam == '':
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
    args = event.pattern_match.group(1)
    chat = event.chat
    user = event.sender
    message = event.message
    if event.is_private:
        await event.reply(
            "Federations can only be deleted by privately messaging me.")
        return
    if args:
        is_fed_id = args[0]
        getinfo = sql.get_fed_info(is_fed_id)
        if getinfo is False:
            await event.reply(
                "This federation does not exist.")
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
        "You sure you want to delete your federation? This cannot be reverted, you will lose your entire ban list, and '{}' will be permanently lost."
        .format(getinfo['fname']),
        buttons=[[Button.inline("⚠️ Delete Federation", data="rmfed_{}".format(fed_id))], [Button.inline("Cancel", data="rmfed_cancel")]], reply_to=message.id)
