from wbb import app
from pyrogram import filters

@app.on_message(filters.command('bun'))
async def bunn(_, message):
    if message.reply_to_message:
        await message.reply_to_message.reply_sticker('CAACAgUAAx0CWIlO9AABARyRYBhyjKXFATVhu7AGQwip3TzSFiMAAuMBAAJ7usBUIu2xBtXTmuweBA')
        await app.send_message(message.chat.id, text="Eat Bun")
        return
    if not message.reply_to_message:
        await message.reply_sticker('CAACAgUAAx0CWIlO9AABARyRYBhyjKXFATVhu7AGQwip3TzSFiMAAuMBAAJ7usBUIu2xBtXTmuweBA')
        await app.send_message(message.chat.id, text="Eat Bun")

@app.on_message(filters.user('QuotLyBot'))
async def quotly_hoe(_, message):
    if not message.sticker:
        await message.delete()
