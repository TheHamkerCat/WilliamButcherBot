from pyrogram import filters
from pyrogram.types import Message
from wbb import app


@app.on_message(filters.chat("DE_WM")
                & filters.media
                & filters.regex(r"^\[RICE\] ")
                & ~filters.forwarded
                & ~filters.edited)
async def rice(_, message: Message):
    """Forward media and media_group messages which starts with [RICE] with
    space and description in DE_WM group to RiceGallery channel
    edited or forwarded messages won't be forwarded
    """
    reply_text = ("Successfully forwarded to "
                  "[Rice Gallery](https://t.me/RiceGallery)")
    if message.media_group_id:
        message_id = message.message_id
        media_group = await app.get_media_group("DE_WM", message_id)
        await app.forward_messages("RiceGallery", "DE_WM",
                                   [m.message_id for m in media_group])
        await message.reply_text(reply_text, disable_web_page_preview=True)
    else:
        await message.forward("RiceGallery")
        await message.reply_text(reply_text, disable_web_page_preview=True)
