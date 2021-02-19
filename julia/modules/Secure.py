from julia import tbot
from julia.events import register
import secureme
from base64 import b64encode, b64decode
@register(pattern="^/encrypt (.*)")
async def hmm(event):
    cmd = event.pattern_match.group(1)
    Text = cmd
    k = secureme.encrypt(Text)
    await event.reply(k)

@register(pattern="^/decrypt (.*)")
async def hmm(event):
    ok = event.pattern_match.group(1)
    Text = ok
    k = secureme.decrypt(Text)
    await event.reply(k)
