import os
from pyrogram import filters
from wbb.utils.pastebin import paste
from wbb import app
from wbb.core.decorators.errors import capture_err

__MODULE__ = "Paste"
__HELP__ = "/paste - To Paste Replied Text Or Document To Nekobin"


@app.on_message(filters.command("paste") & ~filters.edited)
@capture_err
async def paste_func(_, message):
    if message.reply_to_message:
        app.set_parse_mode("markdown")
        if message.reply_to_message.text:
            m = await message.reply_text("Pasting...")
            content = str(message.reply_to_message.text)
            link = await paste(content)
            await m.delete()
            await app.send_photo(
                    message.chat.id,
                    photo=link + "/preview.png",
                    caption=link
                    )

        elif message.reply_to_message.document:
            if message.reply_to_message.document.file_size > 1048576:
                await message.reply_text("You can only paste files smaller than 1MB.")
                return
            m = await message.reply_text("Pasting...")
            doc_file = await message.reply_to_message.download(file_name='paste.txt')
            i = open(doc_file, "r")
            link = await paste(i.read())
            await m.delete()
            await app.send_photo(
                    message.chat.id,
                    photo=link + "/preview.png",
                    caption=link
                    )
            os.remove(doc_file)
    else:
        await message.reply_text("Reply To A Message With /paste")
