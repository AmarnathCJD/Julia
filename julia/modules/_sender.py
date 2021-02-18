#Test
from julia import tbot, OWNER_ID, DEV_USERS, SUDO_USERS
from julia.events import register
client = tbot
thumb_image_path = "./resources/IMG_20210210_170521_219.jpg"
@register(pattern=r"^/send ?(.*)")
async def Prof(event):
    if event.sender_id == OWNER_ID:
        pass
    elif event.sender_id in DEV_USERS:
        pass
    elif event.sender_id in SUDO_USERS:
        await event.reply("You do not have permissions to run this.")
        return
    else:
        return
    thumb = thumb_image_path
    message_id = event.message.id
    input_str = event.pattern_match.group(1)
    the_plugin_file = "./julia/modules/{}.py".format(input_str)
    message_id = event.message.id
    await event.client.send_file(
            event.chat_id,
            the_plugin_file,
            force_document=True,
            allow_cache=False,
            thumb=thumb,
            reply_to=message_id,
        )
