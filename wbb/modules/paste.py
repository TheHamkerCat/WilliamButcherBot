import os
from pyrogram import filters
from wbb.utils import nekobin
from wbb import app
from wbb.utils.errors import capture_err

__MODULE__ = "Paste"
__HELP__ = "/paste - To Paste Replied Text Or Document To Neokobin"


@app.on_message(filters.command("paste") & ~filters.edited)
@capture_err
async def paste(_, message):
    if message.reply_to_message:
        app.set_parse_mode("markdown")
        if message.reply_to_message.text:
            m = await message.reply_text("```Pasting To Nekobin...```")
            message_get = message.reply_to_message.text
            message_as_str = str(message_get)
            paste_link = await nekobin.neko(message_as_str)
            final_link = f"[Nekobin]({paste_link})"
            await m.edit(final_link, disable_web_page_preview=True)

        elif message.reply_to_message.document:
            if message.reply_to_message.document.file_size > 300000:
                await message.reply_text("You can only paste files smaller than 300KB.")
                return
            m = await message.reply_text("```Pasting To Nekobin...```")
            await message.reply_to_message.download(file_name='paste.txt')
            i = open("downloads/paste.txt", "r")
            paste_link = await nekobin.neko(i.read())
            os.remove('downloads/paste.txt')
            final_link = f"[Nekobin]({paste_link})"
            await m.edit(final_link, disable_web_page_preview=True)
    else:
        await message.reply_text("Reply To A Message With /paste")
