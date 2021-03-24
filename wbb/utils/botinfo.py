BOT_ID = 0
BOT_NAME = ""
BOT_USERNAME = ""
BOT_DC_ID = 0


async def get_info(app):
    global BOT_ID, BOT_NAME, BOT_USERNAME, BOT_DC_ID
    getme = await app.get_me()
    BOT_ID = getme.id

    if getme.last_name:
        BOT_NAME = getme.first_name + " " + getme.last_name
    else:
        BOT_NAME = getme.first_name
    BOT_USERNAME = getme.username
    BOT_DC_ID = getme.dc_id
