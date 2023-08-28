from wbb import app 
from wbb import db
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message, Chat

approvaldb = db.autoapprove

# For /help menu
__MODULE__ = "Autoapprove"
__HELP__ = """
command: /autoapprove

This module helps to automatically accepts join request send by a user through invitation link of your group"""



@app.on_message(filters.command("autoapprove", prefixes="/") & filters.group)
async def approval_command(client, message):
    chat_id = message.chat.id
    admin = await app.get_chat_member(chat_id, message.from_user.id)
    if admin.status ==  ChatMemberStatus.OWNER or admin.status == ChatMemberStatus.ADMINISTRATOR:
        if approvaldb.count_documents({"chat_id": chat_id}) > 0:
            keyboard_OFF = InlineKeyboardMarkup([[InlineKeyboardButton("Turn OFF", callback_data="approval_off")]])
            await message.reply("**Autoapproval for this chat is enabled.**", reply_markup=keyboard_OFF)
        else:
            keyboard_ON = InlineKeyboardMarkup([[InlineKeyboardButton("Turn ON", callback_data="approval_on")]])
            await message.reply("**Autoapproval for this chat is disabled.**", reply_markup=keyboard_ON)
    else:
        await message.reply("**You need to be a group administrator to use this command.**")
        return


@app.on_callback_query(filters.regex("approval(.*)"))
async def approval_cb(client, cb):
    chat_id = cb.message.chat.id
    admin = await app.get_chat_member(chat_id, cb.from_user.id)
    if admin.status == ChatMemberStatus.OWNER or admin.status == ChatMemberStatus.ADMINISTRATOR:
        command_parts = cb.data.split("_", 1)
        option = command_parts[1]
        if option == "on":
            if approvaldb.count_documents({"chat_id": chat_id}) == 0:
                approvaldb.insert_one({"chat_id": chat_id})
                keyboard_OFF = InlineKeyboardMarkup([[InlineKeyboardButton("Turn OFF", callback_data="approval_off")]])
                await cb.edit_message_text("**Autoapproval for this chat is enabled.**", reply_markup=keyboard_OFF)
        elif option == "off":
            if approvaldb.count_documents({"chat_id": chat_id}) > 0:
                approvaldb.delete_one({"chat_id": chat_id})
                keyboard_ON = InlineKeyboardMarkup([[InlineKeyboardButton("Turn ON", callback_data="approval_on")]])
                await cb.edit_message_text("**Autoapproval for this chat is disabled.**", reply_markup=keyboard_ON)
    else:
        await cb.answer("This is not for you :-_-:", show_alert=True)


@app.on_chat_join_request(filters.group)
async def autoapprove(client, message: ChatJoinRequest):
    chat=message.chat 
    user=message.from_user
    if approvaldb.count_documents({"chat_id": chat.id}) > 0:
        await app.approve_chat_join_request(chat_id=chat.id, user_id=user.id)
