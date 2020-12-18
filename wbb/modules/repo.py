from wbb import app
from wbb.utils import cust_filter
import requests

__MODULE__ = "Repo"
__HELP__ = "/repo - To Get My Github Repository Link"

api = 'https://api.github.com/repos/thehamkercat/' \
      'WilliamButcherBot/stats/contributors'

print(api)


@app.on_message(cust_filter.command(commands=("repo")))
async def repo(client, message):
    app.set_parse_mode("markdown")
    profile_url = []
    username = []

# Get The List Of Usernames And Profile Url
    for item in requests.get(api).json():
        profile_url.append(f"{item['author']['html_url']}")
        username.append(f"{item['author']['login']}")

# Join Usernames And Profile Url For Markdown
    no_of_contributors = len(username)
    i = 0
    n = 1
    contributors = ""
    while i < no_of_contributors:
        contributors += f"[{n}. {username[i]}]({profile_url[i]})\n"
        n += 1
        i += 1

    await message.reply_text(f'''
```Devs and Contributors```
{contributors}
```Source Code```[Github](https://github.com/thehamkercat/WilliamButcherBot)
''', disable_web_page_preview=True)
