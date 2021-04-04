from wbb import app
from wbb.utils.filter_groups import antiflood_group
from wbb.utils.errors import capture_err
from wbb.utils.dbfunctions import (
    is_antiflood_on,
    antiflood_on,
    antiflood_off
)
from wbb.modules.admin import list_admins, member_permissions
from pyrogram import filters

tdb = []


@app.on_message(group=antiflood_group)
async def antiflood_check(_, message):
    global tdb
    if not is_antiflood_on:
        return
    chat_id = message.chat.id
    user_id = message.from_user.id
    admins = await list_admins(chat_id)

    # ignore admins
    if user_id in admins:
        return
    for chat in tdb:
        if chat['chat_id'] == chat_id:
            for user in chat['user_ids']:
                if user == user_id:
                    chat['user_ids'][user]['messages'] == \
                        ((chat['user_ids'][user]['messages'] + 1)) \
                        if chat['user_ids'][user]['messages'] else 1
                    if chat['user_ids'][user]['messages'] > 7:
                        await message.chat.restrict_member(
                            user_id,
                            permissions=ChatPermissions()
                        )
                        await message.reply_text(f"Yeah i don't like spam, Muted!")
                        return

    if not tdb:
        tdb.append(
            {
                "chat_id": chat_id,
                "user_ids": [
                    {
                        user_id: {
                            "messages": 1
                        }
                    }
                ]
            }
        )
        return


@app.on_message(filters.command("flood"))
@capture_err
async def captcha_state(_, message):
    usage = "**Usage:**\n/flood [ON|OFF]"
    if len(message.command) != 2:
        await message.reply_text(usage)
        return
    user_id = message.from_user.id
    chat_id = message.chat.id
    permissions = await member_permissions(chat_id, user_id)
    if "can_restrict_members" not in permissions:
        await message.reply_text("You don't have enough permissions.")
        return
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "on":
        await antiflood_on(chat_id)
        await message.reply_text("Muting members on 7 consecutive messages.")
    elif state == "off":
        await antiflood_off(chat_id)
        await message.reply_text("Disabled Antiflood")
    else:
        await message.reply_text(usage)
