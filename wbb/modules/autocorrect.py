from pyrogram import filters
from pyrogram.types import Message

from wbb import SUDOERS, USERBOT_ID, USERBOT_PREFIX, app, app2, arq
from wbb.utils.filter_groups import autocorrect_group


@app.on_message(filters.command("autocorrect"))
async def autocorrect_bot(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a text message.")
    reply = message.reply_to_message
    text = reply.text or reply.caption
    if not text:
        return await message.reply_text("Reply to a text message.")
    data = await arq.spellcheck(text)
    if not data.ok:
        return await message.reply_text("Something wrong happened.")
    result = data.result
    await message.reply_text(result.corrected if result.corrected else "Empty")


IS_ENABLED = False


@app2.on_message(
    filters.command("autocorrect", prefixes=USERBOT_PREFIX)
    & filters.user(SUDOERS)
)
async def autocorrect_ubot_toggle(_, message: Message):
    global IS_ENABLED
    if len(message.command) != 2:
        return await message.edit("Not enough arguments.")
    state = message.text.split(None, 1)[1].strip().lower()
    if state == "enable":
        IS_ENABLED = True
        await message.edit("Enabled!")
    elif state == "disable":
        IS_ENABLED = False
        await message.edit("Disabled!")
    else:
        return await message.edit("Wrong argument, Pass (ENABLE|DISABLE).")


@app2.on_message(
    filters.text & ~filters.edited & filters.user(USERBOT_ID),
    group=autocorrect_group,
)
async def autocorrect_ubot(_, message: Message):
    if not IS_ENABLED:
        return
    text = message.text
    data = await arq.spellcheck(text)
    corrected = data.result.corrected
    if corrected == text:
        return
    await message.edit(corrected)
