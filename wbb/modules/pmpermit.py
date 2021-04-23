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

from wbb import app, app2, BOT_ID, USERBOT_ID, SUDOERS
from pyrogram import filters
from wbb.utils.dbfunctions import is_pmpermit_approved, approve_pmpermit, disapprove_pmpermit
from wbb.modules.chatbot import active_chats_ubot

flood = {}


@app2.on_message(filters.private & ~filters.edited & ~filters.me & ~filters.user(SUDOERS))
async def pmpermit_func(_, message):
    user_id = message.from_user.id
    async for m in app2.iter_history(user_id, limit=10):
        if m.reply_markup:
            await m.delete()
    if await is_pmpermit_approved(user_id):
        return
    if str(user_id) in flood:
        flood[str(user_id)] += 1
    else:
        flood[str(user_id)] = 1
    if flood[str(user_id)] > 5:
        await app2.block_user(user_id)
        await message.reply_text("SPAM DETECTED, USER BLOCKED.")
        return
    results = await app2.get_inline_bot_results(BOT_ID, "pmpermit")
    await app2.send_inline_bot_result(
            user_id,
            results.query_id,
            results.results[0].id,
            hide_via=True
            )


@app2.on_message(filters.command("approve", prefixes=".") & filters.user(SUDOERS) & ~filters.via_bot)
async def pm_approve(_, message):
    if not message.reply_to_message:
        await message.edit("Reply to a user's message to approve.")
        return
    user_id = message.reply_to_message.from_user.id
    if await is_pmpermit_approved(user_id):
        await message.edit("User is already approved to pm")
        return
    await approve_pmpermit(user_id)
    await message.edit("User is approved to pm")


@app2.on_message(filters.command("disapprove", prefixes=".") & filters.user(SUDOERS) & ~filters.via_bot)
async def pm_disapprove(_, message):
    if not message.reply_to_message:
        await message.edit("Reply to a user's message to approve.")
        return
    user_id = message.reply_to_message.from_user.id
    if not await is_pmpermit_approved(user_id):
        await message.edit("User is already disapproved to pm")
        return
    await disapprove_pmpermit(user_id)
    await message.edit("User is disapproved to pm")


@app2.on_message(filters.command("block", prefixes=".") & filters.user(SUDOERS) & ~filters.via_bot)
async def block_user_func(_, message):
    if not message.reply_to_message:
        await message.edit("Reply to a user's message to approve.")
        return
    user_id = message.reply_to_message.from_user.id
    await app2.block_user(user_id)
    await message.edit("Successfully blocked the user")


@app2.on_message(filters.command("unblock", prefixes=".") & filters.user(SUDOERS) & ~filters.via_bot)
async def unblock_user_func(_, message):
    if not message.reply_to_message:
        await message.edit("Reply to a user's message to approve.")
        return
    user_id = message.reply_to_message.from_user.id
    await app2.unblock_user(user_id)
    await message.edit("Successfully Unblocked the user")


""" CALLBACK QUERY HANDLER """


@app.on_callback_query(filters.regex("pmpermit"))
async def pmpermit_cq(_, cq):
    global active_chats_ubot
    user_id = cq.from_user.id
    if user_id == USERBOT_ID:
        await cq.answer("It's For The Other Person.")
        return
    data = cq.data.split(None, 1)[1]
    if data == "to_scam_you":
        async for m in app2.iter_history(user_id, limit=10):
            if m.reply_markup:
                await m.delete()
        await app2.send_message(user_id, "Blocked, Go scam someone else.")
        await app2.block_user(user_id)

    elif data == "approve_me":
        await app2.send_message(user_id, "I'm busy right now, will approve you shortly, DO NOT SPAM.")

    elif data == "chitchats":
        await approve_pmpermit(user_id)
        active_chats_ubot.append(user_id)
        await app2.send_message(user_id, "Hello")
