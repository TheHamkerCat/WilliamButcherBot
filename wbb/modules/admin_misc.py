from pyrogram import filters
from wbb import SUDOERS, app
from wbb.utils.errors import capture_err
from wbb.modules.admin import list_admins, member_permissions
import os

__MODULE__ = "Admin Miscs"
__HELP__ = """
/set_chat_title - Change The Name Of A Group/Channel.
/set_chat_photo - Change The PFP Of A Group/Channel.
/set_user_title - Change The Administrator Title Of An Admin.
"""
@app.on_message(filters.command("set_chat_title") & ~filters.private)
@capture_err
async def set_chat_title(_, message):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        permissions = await member_permissions(chat_id, user_id)
        if "can_change_info" not in permissions:
            await message.reply_text("You Don't Have Enough Permissions.")
            return
        if len(message.command) < 2:
            await message.reply_text("**Usage:**\n/set_chat_title NEW NAME")
            return
        old_title = message.chat.title
        new_title = message.text.split(None ,1)[1]
        await message.chat.set_title(new_title)
        await message.reply_text(f"Successfully Changed Group Title From {old_title} To {new_title}")
    except Exception as e:
        print(e)
        await message.reply_text(e)


@app.on_message(filters.command("set_user_title") & ~filters.private)
@capture_err
async def set_user_title(_, message):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        from_user = message.reply_to_message.from_user
        permissions = await member_permissions(chat_id, user_id)
        if "can_change_info" not in permissions:
            await message.reply_text("You Don't Have Enough Permissions.")
            return
        if len(message.command) < 2:
            await message.reply_text("**Usage:**\n/set_user_title NEW ADMINISTRATOR TITLE")
            return
        title = message.text.split(None ,1)[1]
        await app.set_administrator_title(chat_id, from_user.id, title)
        await message.reply_text(f"Successfully Changed {from_user.mention}'s Admin Title To {title}")
    except Exception as e:
        print(e)
        await message.reply_text(e)


@app.on_message(filters.command("set_chat_photo") & ~filters.private)
@capture_err
async def set_chat_photo(_, message):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        permissions = await member_permissions(chat_id, user_id)
        if "can_change_info" not in permissions:
            await message.reply_text("You Don't Have Enough Permissions.")
            return
        if not message.reply_to_message:
            await message.reply_text("Reply to a photo to set it as chat_photo")
            return
        if not message.reply_to_message.photo and not message.reply_to_message.document:
            await message.reply_text("Reply to a photo to set it as chat_photo")
            return
        photo = await message.reply_to_message.download()
        await message.chat.set_photo(photo)
        await message.reply_text(f"Successfully Changed Group Photo")
        os.remove(photo)
    except Exception as e:
        print(e)
        await message.reply_text(e)
