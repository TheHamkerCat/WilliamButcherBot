from wbb import app, SUDOERS, spamwatch
from pyrogram import filters
from wbb.utils.dbfunctions import is_gbanned_user, user_global_karma
import os
import traceback

__MODULE__ = "Info"
__HELP__ = "/info [USERNAME|ID] - Get info about a user."


async def get_user_info(user):
    user = await app.get_users(user)
    user_id = user.id
    username = user.username
    first_name = user.first_name
    mention = user.mention("Link")
    status = user.status
    dc_id = user.dc_id
    photo_id = user.photo.big_file_id if user.photo else None
    is_gbanned = await is_gbanned_user(user_id)
    is_sudo = user_id in SUDOERS
    karma = await user_global_karma(user_id)
    banned_in_spamwatch = False if spamwatch.get_ban(
        user_id) == False else True
    caption = f"""
**ID:** `{user_id}`
**DC:** {dc_id}
**Name:** {first_name}
**Username:** {("@" + username) if username else None}
**Permalink:** {mention}
**Status:** {status}
**Sudo:** {is_sudo}
**Karma:** {karma}
**Gbanned:** {is_gbanned}
**Spamwatch Restricted:** {banned_in_spamwatch}
"""
    return [caption, photo_id]


@app.on_message(filters.command("info"))
async def info_func(_, message):
    try:
        if message.reply_to_message:
            user = message.reply_to_message.from_user.id
        elif not message.reply_to_message and len(message.command) == 1:
            user = message.from_user.id
        elif not message.reply_to_message and len(message.command) != 1:
            user = message.text.split(None, 1)[1]
        info_caption, photo_id = await get_user_info(user)
        if not photo_id:
            await app.send_message(message.chat.id, text=info_caption)
            return
        photo = await app.download_media(photo_id)
        await app.send_photo(message.chat.id, photo=photo, caption=info_caption)
        os.remove(photo)
    except Exception as e:
        await message.reply_text(str(e))
        e = traceback.format_exc()
        print(e)
