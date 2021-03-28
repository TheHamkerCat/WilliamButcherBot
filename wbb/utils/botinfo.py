BOT_ID = 0
BOT_NAME = ""
BOT_USERNAME = ""
BOT_DC_ID = 0
USERBOT_ID = 0
USERBOT_NAME = ""
USERBOT_USERNAME = ""
USERBOT_DC_ID = 0


async def get_info(app, app2):
    global BOT_ID, BOT_NAME, BOT_USERNAME, BOT_DC_ID
    getme = await app.get_me()
    getme2 = await app2.get_me()
    BOT_ID = getme.id
    USERBOT_ID = getme2.id
    if getme.last_name:
        BOT_NAME = getme.first_name + " " + getme.last_name
    else:
        BOT_NAME = getme.first_name
    BOT_USERNAME = getme.username
    BOT_DC_ID = getme.dc_id
    
    if getme2.last_name:
        USERBOT_NAME = getme2.first_name + " " + getme2.last_name
    else:
        USERBOT_NAME = getme2.first_name
    USERBOT_USERNAME = getme2.username
    USERBOT_DC_ID = getme2.dc_id
