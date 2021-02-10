from julia.Config import Config
from julia.events import register
from julia import CMD_HELP
from julia import tbot
from julia import TEMP_DOWNLOAD_DIRECTORY as TMP_DOWNLOAD_DIRECTORY
from telethon import events
import os
from PIL import Image
from glitch_this import ImageGlitcher
from telethon import functions, types

@register(pattern="^/glitch(?: |$)(.*)")
async def glitch(tele):
    cmd = tele.pattern_match.group(1)
    teleinput = tele.pattern_match.group(2)
    reply = await tele.get_reply_message()
    teleid = tele.reply_to_msg_id
    tele = await tele.reply("Hahaha.... GlitchingðŸ¤ª")
    if not (reply and (reply.media)):
        await tele.edit("`Media not found...`")
        return
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    telesticker = await reply.download_media(file="./temp/")
    if not telesticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg")):
        os.remove(telesticker)
        await tele.edit("`Media not found...`")
        return
    os.path.join("./temp/", "glitch.png")
    if teleinput:
        if not teleinput.isdigit():
            await tele.edit("`You input is invalid, check help`")
            return
        teleinput = int(teleinput)
        if not 0 < teleinput < 9:
            await tele.edit("`Invalid Range...`")
            return
    else:
        teleinput = 2
    if telesticker.endswith(".tgs"):
        telefile = os.path.join("./temp/", "glitch.png")
        telecmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {telesticker} {telefile}"
        )
        stdout, stderr = (await runcmd(telecmd))[:2]
        if not os.path.lexists(telefile):
            await tele.edit("`telesticker not found...`")
            LOGS.info(stdout + stderr)
        glitch_file = telefile
    elif telesticker.endswith(".webp"):
        telefile = os.path.join("./temp/", "glitch.png")
        os.rename(telesticker, telefile)
        if not os.path.lexists(telefile):
            await tele.edit("`telesticker not found... `")
            return
        glitch_file = telefile
    elif telesticker.endswith(".mp4"):
        telefile = os.path.join("./temp/", "glitch.png")
        await take_screen_shot(telesticker, 0, telefile)
        if not os.path.lexists(telefile):
            await tele.edit("```telesticker not found...```")
            return
        glitch_file = telefile
    else:
        glitch_file = telesticker
    glitcher = ImageGlitcher()
    img = Image.open(glitch_file)
    if cmd == "glitchs":
        glitched = "./temp/" + "glitched.webp"
        glitch_img = glitcher.glitch_image(img, teleinput, color_offset=True)
        glitch_img.save(glitched)
        await borg.send_file(tele.chat_id, glitched, reply_to=teleid)
        os.remove(glitched)
        await tele.delete()
    elif cmd == "glitch":
        Glitched = "./temp/" + "glitch.gif"
        glitch_img = glitcher.glitch_image(img, teleinput, color_offset=True, gif=True)
        DURATION = 200
        LOOP = 0
        glitch_img[0].save(
            Glitched,
            format="GIF",
            append_images=glitch_img[1:],
            save_all=True,
            duration=DURATION,
            loop=LOOP,
        )
        sandy = await borg.send_file(tele.chat_id, Glitched, reply_to=teleid)
        await borg(
            functions.messages.SaveGifRequest(
                id=types.InputDocument(
                    id=sandy.media.document.id,
                    access_hash=sandy.media.document.access_hash,
                    file_reference=sandy.media.document.file_reference,
                ),
                unsave=True,
            )
        )
        os.remove(Glitched)
        await tele.delete()
    for files in (telesticker, glitch_file):
        if files and os.path.exists(files):
            os.remove(files)
