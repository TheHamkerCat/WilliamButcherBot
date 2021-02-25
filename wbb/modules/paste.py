import os
from pyrogram import filters
from pyrogram.types import Message
from wbb.utils import cust_filter, nekobin
from wbb.utils.errors import capture_err
from wbb import app

__MODULE__ = "Paste"
__HELP__ = "/paste - To Paste Replied Text Or Document To Neokobin"


@app.on_message(cust_filter.command(commands=("paste")) & ~filters.edited)
@capture_err
async def paste(_, message: Message):
    if bool(message.reply_to_message) is True:
        app.set_parse_mode("markdown")
        if bool(message.reply_to_message.text) is True:
            m = await message.reply_text("```Pasting To Nekobin...```")
            message_get = message.reply_to_message.text
            message_as_str = str(message_get)
            paste_link = await nekobin.neko(message_as_str)
            final_link = f"[Nekobin]({paste_link})"
            await m.edit(final_link, disable_web_page_preview=True)

        elif bool(message.reply_to_message.document) is True:
            m = await message.reply_text("```Pasting To Nekobin...```")
            await message.reply_to_message.download(file_name='paste.txt')
            i = open("downloads/paste.txt", "r")
            paste_link = await nekobin.neko(i.read())
            os.remove('downloads/paste.txt')
            final_link = f"[Nekobin]({paste_link})"
            await m.edit(final_link, disable_web_page_preview=True)
    elif bool(message.reply_to_message) is False:
        await message.reply_text(
            "Reply To A Message With /paste, Just Hitting /paste "
            + "Won't Do Anything Other Than Proving Everyone That "
            + "You Are A Spammer Who Is Obsessed To 'BlueTextMustClickofobia")
