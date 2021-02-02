#under development😂
#made by RoseLoverX
from julia import OWNER_ID
from julia.events import register
import asyncio
import os
import sys
from julia import *
async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):

        return isinstance(
            (await
             tbot(functions.channels.GetParticipantRequest(chat,
                                                           user))).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerChat):

        ui = await tbot.get_peer_id(user)
        ps = (await tbot(functions.messages.GetFullChatRequest(chat.chat_id)
                         )).full_chat.participants.participants
        return isinstance(
            next((p for p in ps if p.user_id == ui), None),
            (types.ChatParticipantAdmin, types.ChatParticipantCreator),
        )
    return None

@register(pattern="^/restart$")
async def msg(event):
    check = ups.message.sender_id
    if int(check) != int(OWNER_ID):
        return
    await event.reply(
        "Restarted, Please Wait.. "
    )
    await tbot.disconnect()
    os.execl(sys.executable, sys.executable, *sys.argv)
    quit()
