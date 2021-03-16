from pyrogram import filters
from wbb import app, arq
from wbb.utils.errors import capture_err
from wbb.utils.fetch import fetch

__MODULE__ = "Reddit"
__HELP__ = "/reddit [query] - results something from reddit"


@app.on_message(filters.command("reddit") & ~filters.edited)
@capture_err
async def reddit(_, message):
    if len(message.command) != 2:
        await message.reply_text("/reddit needs an argument")
        return
    subreddit = message.text.split(None, 1)[1]
    try:
        reddit = await arq.reddit(subreddit)
        sreddit = reddit.subreddit
        title = reddit.title
        image = reddit.url
        link = reddit.postLink
        caption = f"""**Title:** `{title}`
**Subreddit:** {sreddit}
**PostLink:** {link}"""
        await message.reply_photo(photo=image, caption=caption)
    except Exception as e:
        print(str(e))
        await message.reply_text(str(e))
