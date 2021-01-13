@register(pattern="^/newfed ?(.*)")
async def _(event):
    chat = event.chat
    user = event.sender
    message = event.message
    if event.is_private:
        await event.reply(
            "Federations can only be created by privately messaging me.")
        return
    if len(message.text) == 1:
        await event.reply("Please write the name of the federation!")
        return
    fednam = message.text.split(None, 1)[1]
    if not fednam == '"':
        fed_id = str(uuid.uuid4())
        fed_name = fednam
        #LOGGER.info(fed_id)

        x = sql.new_fed(user.id, fed_name, fed_id)
        if not x:
            await event.reply(
                "Can't create federation!\nPlease contact @MissJuliaRobotSupport if the problem persists."
            )
            return
            
        await event.reply("**You have succeeded in creating a new federation!**"\
                 "\nName: `{}`"\
                 "\nID: `{}`"
                 "\n\nUse the command below to join the federation:"
                 "\n`/joinfed {}`".format(fed_name, fed_id, fed_id), parse_mode="markdown")
    else:
        await event.reply("Please write down the name of the federation")

