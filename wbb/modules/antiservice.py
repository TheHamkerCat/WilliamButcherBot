# Written By [MaskedVirus | swatv3nub] for William and Ryūga
# Kang With Proper Credits

from wbb import app
from pyrogram import filters
from wbb.modules.admin import list_admins as admemez

__MODULE__ = "AntiService"
__HELP__ = f"""
Plugin to delete antiservice messages in a chat!

/antiservice [enable|disable]
"""

active_chats = []

@app.on_message(filters.command("antiservice") & ~filters.edited)
async def anti_service(_, message):
    global active_chats
    if message.from_user.id not in admemez:
        await message.reply_text("You are Not an Admin!")
        return
    if len(message.command) != 2:
        await message.reply_text("/antiservice [enable | disable]")
        return
    status = message.text.split(None, 1)[1]
    chat_id = message.chat.id
    
    if status == "ENABLE" or status == "enable" or status == "Enable":
        if chat_id not in active_chats:
            active_chats.append(chat_id)
            await message.reply_text("Enabled AntiService System. I will Be Deleting Every Service Message from Now on.")
            return
        await message.reply_text("AntiService System is Already Enabled")
    
    elif status == "DISABLE" or status == "disable" or status == "Disable":
        if chat_id in active_chats:
            active_chats.remove(chat_id)
            await message.reply_text("Disabled AntiService System. I won't Be Deleting Service Message from Now on.")
            return
            await message.reply_text("AntiService System was Never Enabled! How can I Disable it?")
    else:
        await message.reply_text("Unknown Suffix, Use /antiservice [enable|disable]")



@app.on_message(filters.service, group=11)
async def delete_service(_, message):
    chat_id = message.chat.id
    try:
        if chat_id in active_chats:
            await message.delete()
            return
    except:
        pass
