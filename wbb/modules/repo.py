from pyrogram import filters
from wbb import app
from wbb.utils.errors import capture_err
from wbb.utils.fetch import fetch

__MODULE__ = "Repo"
__HELP__ = "/repo - To Get My Github Repository Link " \
           "And Support Group Link"


@app.on_message(filters.command("repo") & ~filters.edited)
@capture_err
async def repo(_, message):
    users = await fetch("https://api.github.com/repos/thehamkercat/williambutcherbot/contributors")
    list_of_users = ""
    count = 1    
    for user in users:
        list_of_users += f"**{count}.** [{user['login']}]({user['html_url']})\n"
        count += 1

    text = f"""[Github](https://github.com/thehamkercat/WilliamButcherBot) | [Group](t.me/PatheticProgrammers)
```----------------
| Contributors |
----------------```
{list_of_users}"""
    await app.send_message(message.chat.id, text=text, disable_web_page_preview=True)
