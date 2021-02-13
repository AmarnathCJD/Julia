import aiohttp
import asyncio
import re
from julia import TOKEN as bot_token
from julia import OWNER_ID as owner_id
from julia import BOT_ID as bot_id
from pyrogram import Client, filters
from julia import register
luna = Client(
    ":memory:",
    bot_token=bot_token,
    api_id=6,
    api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e",
)

blacklisted = []


async def getresp(query):
    url = f"https://lunabot.tech/?query={query}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            res = await res.json()
            text = res["response"]
            return text

@register(pattern="^/truth$")
async def start(_, message):
    user_id = message.from_user.id
    if user_id in blacklisted:
        return
    await luna.send_chat_action(message.chat.id, "typing")
    await message.reply_text(
        "**Only For Owners**\n/shutdown - `Shutdown Luna.`\n/blacklist - `Blacklist A User.`\n/whitelist - `Whitelist A User.`"
    )

