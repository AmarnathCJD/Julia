from selenium import webdriver
import io
import traceback
from datetime import datetime

from julia import tbot
from julia.events import register




async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):

        return isinstance(
            (await
             tbot(functions.channels.GetParticipantRequest(chat,
                                                           user))).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerChat):

        ui = await tbot.get_peer_id(user)
        ps = (await tbot(functions.messages.GetFullChatRequest(chat.chat_id)
                         )).full_chat.participants.participants
        return isinstance(
            next((p for p in ps if p.user_id == ui), None),
            (types.ChatParticipantAdmin, types.ChatParticipantCreator),
        )
    return None

@register(pattern="^/ss ?(.*)")
async def _(event):
    HELP_STR = "use `/rmbg` as reply to a media"
    if event.fwd_from:
        return
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if event.is_group:
        if (await is_register_admin(event.input_chat, event.message.sender_id)):
            pass
        elif event.chat_id == iid and event.sender_id == userss:
            pass
        else:
            return
    if Config.GOOGLE_CHROME_BIN is None:
        await event.edit("need to install Google Chrome. Module Stopping.")
        return
    await event.edit("Processing ...wait")
    start = datetime.now()
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--test-type")
        chrome_options.add_argument("--headless")
        # https://stackoverflow.com/a/53073789/4723940
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.binary_location = Config.GOOGLE_CHROME_BIN
        await event.edit("Starting Google Chrome BIN")
        driver = webdriver.Chrome(chrome_options=chrome_options)
        input_str = event.pattern_match.group(1)
        imp = "anie"
        driver.get(input_str)
        await event.edit("Calculating Page Dimensions")
        height = driver.execute_script(
            "return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);"
        )
        width = driver.execute_script(
            "return Math.max(document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth);"
        )
        await event.edit("Painting web-page")
        driver.set_window_size(width + 100, height + 100)
        # Add some pixels on top of the calculated dimensions
        # for good measure to make the scroll bars disappear
        im_png = driver.get_screenshot_as_png()
        # saves screenshot of entire page
        driver.close()
        await event.edit("Stopping Google Chrome BIN")
        message_id = event.message.id
        if event.reply_to_msg_id:
            message_id = event.reply_to_msg_id
        with io.BytesIO(im_png) as out_file:
            out_file.name = "Anie.sshot.PNG"
            await borg.send_file(
                event.chat_id,
                out_file,
                caption=imp,
                force_document=True,
                reply_to=message_id,
                allow_cache=False,
                silent=True,
            )
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit(f"Done in {ms} seconds")
    except Exception:
        await event.edit(traceback.format_exc())

