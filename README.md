# ✨ WilliamButcherBot ✨
### Telegram Group Manager Bot + Userbot Written In Python Using Pyrogram.


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[![Python](http://forthebadge.com/images/badges/made-with-python.svg)](https://python.org)&nbsp;
[![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://GitHub.com/TheHamkerCat/)


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![LICENSE](https://img.shields.io/github/license/thehamkercat/WilliamButcherBot?style=for-the-badge&logo=appveyor)&nbsp;
![Contributors](https://img.shields.io/github/contributors/thehamkercat/WilliamButcherBot?style=for-the-badge&logo=appveyor)&nbsp;
![Repository Size](https://img.shields.io/github/repo-size/thehamkercat/WilliamButcherBot?style=for-the-badge&logo=appveyor)


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Python Version](https://img.shields.io/badge/python-3.8-green?style=for-the-badge&logo=appveyor)&nbsp;
![Issues](https://img.shields.io/github/issues/thehamkercat/WilliamButcherBot?style=for-the-badge&logo=appveyor)&nbsp;
![Forks](https://img.shields.io/github/forks/thehamkercat/WilliamButcherBot?style=for-the-badge&logo=appveyor)&nbsp;
![Stars](https://img.shields.io/github/stars/thehamkercat/WilliamButcherBot?style=for-the-badge&logo=appveyor)



<img src="https://static2.aniimg.com/upload/20170515/414/c/d/7/cd7EEF.jpg" width="300" align="right">

## Ready to use method

A ready-to-use running instance of this bot can be found on 
telegram as [WilliamButcherBot](https://t.me/WilliamButcherBot)

## Requirements

- Python == 3.9
- A [Telegram API key](https://docs.pyrogram.org/intro/setup#api-keys).
- A [Telegram bot token](https://t.me/botfather).
- A [MongoDB URI](https://telegra.ph/How-To-get-Mongodb-URI-04-06)


## Install Locally Or On A VPS

```sh
$ git clone https://github.com/thehamkercat/WilliamButcherBot

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
$ git clone https://github.com/TheHamkerCat/WilliamButcherBot

$ cd WilliamButcherBot

$ pip3 install pyrogram TgCrypto

$ python3 str_gen.py
```

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/thehamkercat/WilliamButcherBot/)


# Docker

```sh
$ git clone https://github.com/TheHamkerCat/WilliamButcherBot

$ cd WilliamButcherBot

$ cp sample_config.env config.env
```
Edit **config.env** with your own values

```sh
$ sudo docker build . -t wbb

$ sudo docker run wbb
```

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

## Note

1. Support Chat: [WbbSupport](https://t.me/wbbsupport)
