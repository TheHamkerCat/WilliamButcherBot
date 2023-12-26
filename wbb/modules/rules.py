"""
MIT License

Copyright (c) 2023 SI_NN_ER_LS 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from wbb import BOT_USERNAME, app
from wbb.core.decorators.permissions import adminsOnly
from wbb.core.keyboard import ikb
from wbb.modules.admin import member_permissions
from wbb.modules.notes import extract_urls
from wbb.utils.dbfunctions import delete_rules, get_rules, set_chat_rules
from wbb.utils.functions import check_format

__MODULE__ = "Rules"
__HELP__ = """
 • `/rules`: get the rules for this chat.

**Admins only:**
 • `/setrules`: Reply to a message to set the rules for the chat.
 • `/clearrules`: clear the rules for this chat.
"""


@app.on_message(filters.command("rules") & ~filters.private)
async def send_rules(_, message):
    chat_id = message.chat.id
    replied_message = message.reply_to_message
    if replied_message:
        message = replied_message
    await message.reply_text(
        "**Click on the button to see the chat rules!**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "rules",
                        url=f"t.me/{BOT_USERNAME}?start=rules_{chat_id}",
                    )
                ]
            ]
        ),
    )


@app.on_message(filters.command("setrules") & ~filters.private)
@adminsOnly("can_change_info")
async def set_rules(_, message):
    try:
        chat_id = message.chat.id
        replied_message = message.reply_to_message
        if len(message.command) < 2 and not replied_message:
            return await message.reply(
                "**Reply to a message to set new rules.**"
            )
        if len(message.command) < 2 and replied_message.text:
            rules = replied_message.text.markdown
            if replied_message.reply_markup:
                urls = extract_urls(replied_message.reply_markup)
                if urls:
                    response = "\n".join(
                        [f"{name}=[{text}, {url}]" for name, text, url in urls]
                    )
                    rules = rules + response
        else:
            text = message.text.markdown
            rules = text.split(" ", 1)[1]
        rules = await check_format(ikb, rules)
        if not rules:
            return await message.reply_text(
                "**Wrong formatting, check the help section.**"
            )
        await set_chat_rules(chat_id, rules)
        return await message.reply_text(
            "**Successfully set new rules for this chat.**"
        )
    except Exception:
        await message.reply_text(
            "**You can only set text messages as rules.**"
        )


@app.on_message(filters.command("clearrules") & ~filters.private)
@adminsOnly("can_change_info")
async def delete_rules_cmd(_, message):
    rules = await get_rules(message.chat.id)
    if not rules:
        await message.reply_text("**No rules in this chat.**")
    else:
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "YES, DO IT", callback_data="drules_yes"
                    ),
                    InlineKeyboardButton("Cancel", callback_data="drules_no"),
                ]
            ]
        )
        await message.reply_text(
            "**Are you sure to delete the current rules ?.**",
            reply_markup=keyboard,
        )


@app.on_callback_query(filters.regex("drules_(.*)"))
async def delete_rules_cb(_, cb):
    chat_id = cb.message.chat.id
    from_user = cb.from_user
    permissions = await member_permissions(chat_id, from_user.id)
    permission = "can_change_info"
    if permission not in permissions:
        return await cb.answer(
            f"You don't have the required permission.\n Permission: {permission}",
            show_alert=True,
        )
    input = cb.data.split("_", 1)[1]
    if input == "yes":
        deleted = await delete_rules(chat_id)
        if deleted:
            return await cb.message.edit(
                "**Successfully deleted rules of this chat.**"
            )
    if input == "no":
        await cb.message.reply_to_message.delete()
        await cb.message.delete()
