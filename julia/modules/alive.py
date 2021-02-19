from julia import SUDO_USERS, OWNER_ID, tbot, DEV_USERS
from julia.events import register


@register(pattern="^/alive")
async def alive(event):
    if event.sender_id == OWNER_ID:
        await event.reply("I'm Alive Master")
    elif event.sender_id in DEV_USERS:
        await event.reply("I'm Alive Co-Master")
    elif event.sender_id in SUDO_USERS:
        await event.reply("I'm Alive Dad!")
    elif event.sender_id not in SUDO_USERS:
        await event.reply("★彡[ALWAYS OP]彡★")
