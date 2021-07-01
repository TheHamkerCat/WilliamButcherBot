# ✨ Tsuzumi Bot ✨
### Telegram Group Manager Bot + Userbot Written In Python Using Pyrogram.



<img src="https://static2.aniimg.com/upload/20170515/414/c/d/7/cd7EEF.jpg" width="300" align="right">


## Requirements

- Python >= 3.9
- A [Telegram API key](https://docs.pyrogram.org/intro/setup#api-keys).
- A [Telegram bot token](https://t.me/botfather).
- A [MongoDB URI](https://telegra.ph/How-To-get-Mongodb-URI-04-06)


## Install Locally Or On A VPS

```sh
$ git clone https://github.com/nisarga-developer/WilliamButcherBot

$ cd WilliamButcherBot

$ pip3 install -U -r requirements.txt

$ cp sample_config.py config.py
```
Edit **config.py** with your own values

# Run Directly
```sh
$ python3 -m wbb
```

# Run On Heroku

## Generating Pyrogram Session For Heroku

```
$ git clone https://github.com/nisarga-developer/WilliamButcherBot

$ cd WilliamButcherBot

$ pip3 install pyrogram TgCrypto

$ python3 str_gen.py
```

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Nisarga-Developer/WilliamButcherBot/)



## Write new modules

```py
# Add license text here, get it from below

from wbb import app # This is bot's client
from wbb import app2 # userbot client, import it if module is related to userbot
from pyrogram import filters # pyrogram filters
...


# For /help menu
__MODULE__ = "Module Name"
__HELP__ = "Module help message"


@app.on_message(filters.command("start"))
async def some_function(_, message):
    await message.reply_text("I'm already up!!")

# Many useful functions are in, wbb/utils/, wbb, and wbb/core/
```

And put that file in wbb/modules/, restart and test your bot.

# LICENSE

MIT

```
MIT License

Copyright (c) 2021 TheHamkerCat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Note
Tsuzumi Bot can be found here [Tsuzumi](https://telegram.me/TsuzumiBot) 😎
    Tsuzumi is a custom fork of WilliamButcherBot. Thanks to TheHamkerCat. 😀
    [Original WilliamButcherBot Repo](https://github.com/Nisarga-Developer/WilliamButcherBot)
    
