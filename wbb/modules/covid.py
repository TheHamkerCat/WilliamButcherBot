from wbb import app
from wbb.utils.errors import capture_err
from wbb.utils.json_prettify import json_prettify
from wbb.utils.fetch import fetch
from pyrogram import filters


__MODULE__ = "Covid"
__HELP__ = """/covid - To Get Global Stats of Covid.
/covid [COUNTRY] - To Get Stats of A Single Country."""


@app.on_message(filters.command("covid") & ~filters.edited)
@capture_err
async def covid(_, message):
    if len(message.command) == 1:
        data = await fetch("https://corona.lmao.ninja/v2/all")
        data = await json_prettify(data)
        await app.send_message(message.chat.id, text=data)
        return
    if len(message.command) != 1:
        country = message.text.split(None, 1)[1].strip()
        country = country.replace(" ", "")
        data = await fetch(f"https://corona.lmao.ninja/v2/countries/{country}")
        data = await json_prettify(data)
        await app.send_message(message.chat.id, text=data)
        return
