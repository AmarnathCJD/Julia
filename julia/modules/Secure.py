from julia import tbot
from julia.events import register
import secureme

@register(pattern="^/encrypt (.*)")
async def hmm(event):
    cmd = event.pattern_match.group(1)
    Text = cmd
    k = secureme.encrypt(Text)
    await event.reply(k)
