import requests as r
from pyrogram.types import Message
from pyrogram import filters
from wbb import app
from wbb.utils import cust_filter
from wbb.utils.errors import capture_err


__MODULE__ = "Reddit"
__HELP__ = "/reddit [query] - results something from reddit"

@app.on_message(cust_filter.command(commands=("reddit")) & ~filters.edited)
@capture_err
async def reddit(_, message: Message):
    if len(message.command) != 2:
        await message.reply_text("/reddit needs an argument")
        return
    subreddit = message.command[1]
    res = r.get(f"https://meme-api.herokuapp.com/gimme/{subreddit}")
    res = res.json()
    rpage = res.get(str("subreddit"))  # Subreddit
    title = res.get(str("title"))  # Post title
    memeu = res.get(str("url"))  # meme pic url
    plink = res.get(str("postLink"))
    caps = f"<b>Title</b>: {title}\n"
    caps += f"<b>Subreddit: </b>r/{rpage}\n"
    caps += f"<b>PostLink:</b> {plink}"
    await message.reply_photo(photo=memeu, caption=(caps))
