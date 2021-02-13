from userbot import *
from userbot.utils import *
from userbot.cmdhelp import CmdHelp
from telethon.events import NewMessage
from telethon.tl.custom import Dialog
from telethon.tl.types import Channel, Chat, User

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "Royal User"

ludosudo = Config.SUDO_USERS

if ludosudo:
    sudou = "True"
else:
    sudou = "False"

royal = bot.uid

PM_IMG = "https://telegra.ph/file/b3818868fea51e007bae6.jpg"
pm_caption = "__**🔥🔥𝚁𝚘𝚢𝚊𝚕𝚄𝚜𝚎𝚛-𝙱𝚘𝚝🔥🔥**__\n\n"

pm_caption += (
    f"               __↼🄼🄰🅂🅃🄴🅁⇀__\n**『[{DEFAULTUSER}](tg://user?id={royal})』**\n\n"
)

pm_caption += "🛡️TELETHON🛡️ : `1.15.0` \n"

pm_caption += f"😈𝚁𝚘𝚢𝚊𝚕-𝙱𝚘𝚝😈  : __**{royalversion}**__\n"

pm_caption += f"⚜️Sudo⚜️             : `{sudou}`\n"

pm_caption += "⚠️CHANNEL⚠️    : [ᴊᴏɪɴ](https://t.me/RoyalBot_Official)\n"

pm_caption += "🔥CREATOR🔥     : [NOOB HERE](https://t.me/No_Needz_Approval)\n"

pm_caption += "😆OWNER😆        : [NOOB HERE](https://t.me/Apoorvroy86)\n"

pm_caption += "🤩SUPPORTER🤩: [HELLBOY](https://t.me/Kraken_The_BadASS)\n"

pm_caption += "    [✨REPO✨](https://github.com/abhishek61728/ROYALUSER-BOT) 🔹 [📜LICENSE📜](https://github.com/abhishek61728/ROYALUSER-BOT/blob/main/LICENSE)"


@bot.on(admin_cmd(outgoing=True, pattern="alive$"))
@bot.on(sudo_cmd(pattern="alive$", allow_sudo=True))
async def amireallyalive(alive):
    await alive.get_chat()
    await alive.delete()
    """ For .alive command, check if the bot is running.  """
    await borg.send_file(alive.chat_id, PM_IMG, caption=pm_caption)
    await alive.delete()

CmdHelp("alive").add_command(
  'alive', None, 'Check weather the bot is alive or not'
).add_command(
  'royal', None, 'Check weather the bot is alive or not. In your custom Alive Pic and Alive Msg'
).add()
