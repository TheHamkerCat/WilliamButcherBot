from pyrogram import filters
from wbb import app
from wbb.modules.sticker import create_sticker

__MODULE__ = "Quotly"
__HELP__ = "/q - Create Quotly Sticker"


@app.on_message(filters.command('q') & ~filters.edited)
async def qoute_maker(client, message):
    try:
        if message.reply_to_message:
            await create_sticker(client, message.reply_to_message)
        else:
            await create_sticker(client, message)
    except Exception as e:
        print(str(e))
    await message.delete()
