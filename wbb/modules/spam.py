"""
MIT License

Copyright (c) 2021 TheHamkerCat

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
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, Message)

from wbb import LOG_GROUP_ID, SUDOERS, app, arq
from wbb.core.decorators.errors import capture_err
from wbb.modules.admin import list_admins, member_permissions
from wbb.modules.trust import get_spam_data
from wbb.utils.filter_groups import spam_protection_group

__MODULE__ = "AntiSpam"
__HELP__ = """
**Antispam helps protect your group from spam.**

- It's still new so it might be a bit inaccurate.

- Currently, it only alerts for spam and gives you a button to delete the message,
  but in the future, it will delete the spam message automatically.

**Commands:**
    - /spam
        To mark a message as spam, this will help devs to 
        improve spam protection algorithm.

As of now, you cannot turn this off, but we'll add an enable/disable command in the future
"""


@app.on_message(
    (filters.text | filters.caption) & ~filters.private & ~filters.me,
    group=spam_protection_group,
)
async def spam_protection_func(_, message: Message):
    text = message.text or message.caption
    chat_id = message.chat.id
    user = message.from_user
    if not text or not user:
        return

    # We'll handle admins only if it's spam, ignore only sudo users for now.
    if user.id in SUDOERS:
        return
    data = await get_spam_data(message, text)
    if not data.is_spam:
        return
    if user.id in (await list_admins(chat_id)):
        return
    text = f"""
🚨  **SPAM DETECTED** 🚨

**User:** {user.mention}
**Message:** [Link]({message.link})
**Spam Probability:** {data.spam_probability} %
**Action:** Alerted
"""
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Yes it's spam", callback_data="s_p_spam"
                ),
                InlineKeyboardButton(
                    text="No, it's not spam",
                    callback_data="s_p_ham",
                ),
            ],
        ]
    )
    await message.reply_text(
        text=text,
        reply_markup=keyboard,
        disable_web_page_preview=True,
    )


dev_forward = (
    "If you're not a developer of WBB, forward this message to devs, "
    + "so that they can use it to improve spam protection algorithm."
)


@app.on_callback_query(filters.regex("s_p_"))
async def spam_p_callback(_, cq: CallbackQuery):
    from_user = cq.from_user
    chat_id = cq.message.chat.id

    permissions = await member_permissions(chat_id, from_user.id)
    permission = "can_delete_messages"
    if permission not in permissions:
        return await cq.answer(
            "You don't have enough permissions to perform this action.\n"
            + f"Permission needed: {permission}",
            show_alert=True,
        )

    if cq.data.split("_")[-1] == "spam":
        try:
            await cq.message.reply_to_message.delete()
        except Exception:
            await cq.message.delete()
            return
        text = cq.message.text.markdown
        text = text.replace(
            "Alerted", f"Deleted Message With {from_user.mention}'s Approval."
        )
        await cq.message.edit(text)
        if cq.message.reply_to_message:
            text = f"**ADMINS OF {chat_id} FLAGGED THIS MESSAGE AS SPAM**\n\n"
            text += f"`{cq.message.reply_to_message.text.markdown}`\n\n__{dev_forward}__"
            return await app.send_message(
                LOG_GROUP_ID, text, disable_web_page_preview=True
            )
        return

    await cq.message.delete()
    if cq.message.reply_to_message:
        text = f"**ADMINS OF {chat_id} FLAGGED THIS MESSAGE AS NOT SPAM**\n\n"
        text += f"`{cq.message.reply_to_message.text.markdown}`\n\n__{dev_forward}__"
        return await app.send_message(
            LOG_GROUP_ID, text, disable_web_page_preview=True
        )


@app.on_message(filters.command("spam") & ~filters.private)
async def spam_flag_func(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text(
            "Reply to a message to flag it as spam"
        )

    r = message.reply_to_message
    if not r.text and not r.caption:
        return await message.reply_text(
            "Reply to a text message to flag it as spam"
        )

    text = r.text or r.caption
    if not text:
        return await message.reply_text(
            "Reply to a text message to flag it as spam"
        )

    msg = f"""
**ADMINS OF {message.chat.id} FLAGGED THIS MESSAGE AS SPAM**

```
{text.markdown}
```

__{dev_forward}__
"""
    await message.reply_text(
        "Message was flagged as spam, Devs will use it to improve spam protection algorithm."
    )
    await app.send_message(LOG_GROUP_ID, msg, disable_web_page_preview=True)
