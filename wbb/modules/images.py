from wbb.utils import cust_filter
from wbb import app, WALL_API_KEY
import urllib.request
import json
from random import randint
import requests as r

__MODULE__ = "Images"
__HELP__ = "/cat - Get Cute Cats Images\n" + \
           "/dog - Get Cute Dogs Images\n" + \
           "/wall [something] - Get Wallpapers"


@app.on_message(cust_filter.command(commands=("cat")))
async def cat(client, message):
    with urllib.request.urlopen(
        "https://api.thecatapi.com/v1/images/search"
    ) as url:
        data = json.loads(url.read().decode())
    cat_url = (data[0]['url'])
    await message.reply_photo(cat_url)


@app.on_message(cust_filter.command(commands=("dog")))
async def dog(client, message):
    with urllib.request.urlopen(
        "https://api.thedogapi.com/v1/images/search"
    ) as url:
        data = json.loads(url.read().decode())
    dog_url = (data[0]['url'])
    await message.reply_photo(dog_url)


@app.on_message(cust_filter.command(commands=("wall")))
async def wall(client, message):
    app.set_parse_mode("markdown")
    m = await message.reply_text("Searching!")
    try:
        term = (message.text.split(None, 1)[1])
    except IndexError:
        await m.edit("`\"/wall\" needs a keyword argument`")

    api = "https://wall.alphacoders.com/api2.0/get.php?auth=" + \
        "{}&method=search&term={}".format(WALL_API_KEY, term)

    json_rep = r.get(api).json()
    if not json_rep.get("success"):
        await m.edit("FTS! something unusual happened, " +
                     "report to support @Thepirategang")
    else:
        wallpapers = json_rep.get("wallpapers")
        if not wallpapers:
            await m.edit(
                "Found literally nothing!,You should work on your English.")
            return
        else:
            index = randint(0, len(wallpapers) - 1)
            wallpaper = wallpapers[index]
            wallpaper = wallpaper.get("url_image")
            wallpaper = wallpaper.replace("\\", "")
            await message.reply_document(wallpaper)
    await m.delete()
