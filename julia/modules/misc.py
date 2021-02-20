from julia import tbot
from julia.events import register

from telethon import version
from math import ceil
import json
import random
import re
from telethon import events, errors, custom
import io
from platform import python_version, uname 
import os
import time
import asyncio
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins




@register(pattern="^/wish (.*)")
async def wish_check(event):
    wishtxt = event.pattern_match.group(1)
    chance = random.randint(0, 100)
    if wishtxt:
        reslt = f"**Your wish **__{wishtxt}__ **has been cast.** ✨\
              \n\n__Chance of success :__ **{chance}%**"
    else:
        if event.is_reply:
            reslt = f"**Your wish has been cast. **✨\
                  \n\n__Chance of success :__ **{chance}%**"
        else:
            reslt = f"Make A Wish."
    await event.reply(reslt)




normiefont = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
weebyfont = ["Λ", "в", "¢", "∂", "є", "ƒ", "g", "н", "ι", "נ", "к", "ℓ", "м", "η", "σ", "ρ", "q", "я", "ѕ", "т", "υ", "ν", "ω", "χ", "у", "z"]

@register(pattern="^f ?(.*)")
async def weebify(event):
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await event.reply("`What I am Supposed to Fontify U Dumb`")
        return
    string = "".join(args).lower()
    for normiecharacter in string:
        if normiecharacter in normiefont:
            weebycharacter = weebyfont[normiefont.index(normiecharacter)]
            string = string.replace(normiecharacter, weebycharacter)
    await event.reply(string)
