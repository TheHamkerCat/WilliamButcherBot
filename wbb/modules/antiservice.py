# Written By [MaskedVirus | swatv3nub] for William and Ryūga
# Kang With Proper Credits

from wbb import app
from pyrogram import filters
from wbb.modules.admin import member_permissions
from wbb.utils.dbfunctions import is_antiservice_on, antiservice_on, antiservice_off

__MODULE__ = "AntiService"
__HELP__ = """
Plugin to delete service messages in a chat!

/antiservice [enable|disable]
"""


@app.on_message(filters.command("antiservice") & ~filters.private)
async def anti_service(_, message):
    if len(message.command) != 2:
        await message.reply_text("Usage: /antiservice [enable | disable]")
        return
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    chat_id = message.chat.id
    user_id = message.from_user.id
    permissions = await member_permissions(chat_id, user_id)
    if "can_change_info" not in permissions:
        await message.reply_text("You don't have enough permissions.")
        return
    if status == "enable":
        await antiservice_on(chat_id)
        await message.reply_text("Enabled AntiService System. I will Delete Service Messages from Now on.")
    elif status == "disable":
        await antiservice_off(chat_id)
        await message.reply_text("Disabled AntiService System. I won't Be Deleting Service Message from Now on.")
    else:
        await message.reply_text("Unknown Suffix, Use /antiservice [enable|disable]")


@app.on_message(filters.service, group=11)
async def delete_service(_, message):
    chat_id = message.chat.id
    try:
        if await is_antiservice_on(chat_id):
            await message.delete()
            return
    except Exception:
        pass
