"""
GitHub Module
"""
from pyrogram import filters

from wbb import app
from wbb.core.decorators.errors import capture_err

__MODULE__ = "GitHubSS"
__HELP__ = "/githubss | .githubss [Username] or [Username/RepoName] - Take A Screenshot Of A Github Profile or Repo"


@app.on_message(filters.command("githubss"))
@capture_err
async def take_ss(_, message):
    try:
        if len(message.command) != 2:
            return await message.reply_text(
                "That's something invaild"
            )
        url = message.text.split(None, 1)[1]
        m = await message.reply_text("**Taking Screenshot**")
        await m.edit("**Uploading**")
        try:
            await app.send_photo(
                message.chat.id,
                photo=f"https://webshot.amanoteam.com/print?q=https://github.com/{url}",
            )
        except TypeError:
            return await m.edit("Error")
        await m.delete()
    except Exception as e:
        await message.reply_text(str(e))
