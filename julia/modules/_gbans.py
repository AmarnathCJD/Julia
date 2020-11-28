from julia import SUDO_USERS
from julia.events import register

G_BAN_LOGGER_GROUP = "@MissJuliaRobotGbans"

@register(pattern="^/gban ?(.*)")
async def _(event):
    if event.fwd_from:
        return
    if not event.sender_id in SUDO_USERS:
       return
    reason = event.pattern_match.group(1)
    if not reason:
      reason = "No reason given" 
    if event.reply_to_msg_id:
        r = await event.get_reply_message()
        r_sender_id = r.sender_id 
    await event.client.send_message(
            G_BAN_LOGGER_GROUP,
            "**NEW GLOBAL BAN**\n\n**PERMALINK:** [user](tg://user?id={})\n**REASON: {}".format(r_sender_id, reason)
        )
    await event.reply("Gbanned Successfully")


@register(pattern="^/ungban ?(.*)")
async def _(event):
    if Config.G_BAN_LOGGER_GROUP is None:
        await event.edit("ENV VAR is not set. This module will not work.")
        return
    if event.fwd_from:
        return
    reason = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        r = await event.get_reply_message()
        r_sender_id = r.from_id
        await event.client.send_message(
            Config.G_BAN_LOGGER_GROUP,
            "!ungban [user](tg://user?id={}) {}".format(r_sender_id, reason)
        )
    await event.delete()
