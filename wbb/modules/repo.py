from pyrogram.types import Message
from wbb import app
from wbb.utils import cust_filter
from pyrogram import filters

__MODULE__ = "Repo"
__HELP__ = "/repo - To Get My Github Repository Link " \
           "And Support Group Link"


@app.on_message(cust_filter.command(commands=("repo")) & ~filters.edited)
async def repo(_, message: Message):
    app.set_parse_mode("markdown")
    await message.reply_text(
        "[Github](https://github.com/thehamkercat/WilliamButcherBot)"
        + " | [Group](t.me/WBBSupport)", disable_web_page_preview=True)
