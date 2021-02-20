import io
import os
import traceback
from julia import CMD_HELP
from selenium import webdriver
from julia.events import register
from selenium.webdriver.chrome.options import Options
from julia import *
from julia.Config import Config
from julia import tbot
GOOGLE_CHROME_BIN = "/app/.apt/usr/bin/google-chrome"

@register(pattern="^/sshot (.*)")
async def msg(event):
    if event.sender_id in SUDO_USERS:
        pass
    elif event.sender_id == OWNER_ID:
        pass
    else:
        return
    try:
        await event.reply("Painting Web_Page...")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--test-type")
        chrome_options.add_argument("--headless")
        # https://stackoverflow.com/a/53073789/4723940
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.binary_location=GOOGLE_CHROME_BIN
        driver = webdriver.Chrome(chrome_options=chrome_options)
        input_str = event.pattern_match.group(1)
        imp = "anie"
        driver.get(input_str)
        height = driver.execute_script(
            "return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);"
        )
        width = driver.execute_script(
            "return Math.max(document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth);"
        )
        driver.set_window_size(width + 100, height + 100)
        # Add some pixels on top of the calculated dimensions
        # for good measure to make the scroll bars disappear
        im_png = driver.get_screenshot_as_png()
        # saves screenshot of entire page
        driver.close()
        message_id = event.message.id
        if event.reply_to_msg_id:
            message_id = event.reply_to_msg_id
        with io.BytesIO(im_png) as out_file:
            out_file.name = "Anie.sshot.PNG"
            await tbot.send_file(
                event.chat_id,
                out_file,
                caption=imp,
                force_document=True,
                reply_to=message_id,
                allow_cache=False,
                silent=True,
            )
        await event.delete()
    except Exception:
        await event.edit(traceback.format_exc())

file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /sshot: Get Screenshot Of a Website
"""

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})
