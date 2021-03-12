from pyrogram import filters
from wbb import app
from wbb.utils.errors import capture_err

__MODULE__ = "Repo"
__HELP__ = "/repo - To Get My Github Repository Link " \
           "And Support Group Link"


@app.on_message(filters.command("repo") & ~filters.edited)
@capture_err
async def repo(_, message):
    await message.reply_text(
        "[Github](https://github.com/thehamkercat/WilliamButcherBot)"
        + " | [Group](t.me/TheHamkerChat)", disable_web_page_preview=True)
