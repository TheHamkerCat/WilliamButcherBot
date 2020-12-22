from pyrogram import filters
from pyrogram.types import Message
from wbb import app
from wbb.utils import cust_filter


__MODULE__ = "Rice"
__HELP__ = "/rice - To Forward Your Linux Rice To DE_WM's" \
           "Rice Gallery only works in [DE_WM](t.me/de_wm)"


@app.on_message(filters.chat('DE_WM') & cust_filter.command(commands=("rice")))
async def rice(client, message: Message):
    if bool(message.reply_to_message) is True:
        app.set_parse_mode("markdown")
        user_id = message.reply_to_message.from_user.id
        await message.reply_to_message.forward('RiceGallery')
        await message.reply_text(
            f"[Your](tg://user?id={user_id}) Rice Forwared"
            " To [Rice Gallery](https://t.me/RiceGallery)",
            disable_web_page_preview=True)

    elif bool(message.reply_to_message) is False:
        await message.reply_text(
            "Reply To A Message With /rice, Just Hitting /rice "
            + "Won't Do Anything Other Than Proving Everyone That "
            + "You Are A Spammer Who Is Obsessed To 'BlueTextMustClickofobia")
