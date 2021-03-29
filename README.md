# WilliamButcherBot
Just Another Telegram Bot Written In Python Using Pyrogram.

[![Python](http://forthebadge.com/images/badges/made-with-python.svg)](https://python.org)

<img src="https://static2.aniimg.com/upload/20170515/414/c/d/7/cd7EEF.jpg" width="300" align="right">

## Requirements

- Python==3.9.
- Neofetch is needed for some modules.
- A [Telegram API key](https://docs.pyrogram.org/intro/setup#api-keys).
- A [Telegram bot token](https://t.me/botfather).


## Install Locally Or On A VPS

```sh
$ git clone https://github.com/thehamkercat/WilliamButcherBot

$ cd WilliamButcherBot

$ pip3 install -U -r requirements.txt

$ cp sample_config.py config.py
```
Edit **config.py** with your own values

# Run
```sh
$ python3 -m wbb
```

# Heroku

```sh 
$ git clone https://github.com/thehamkercat/WilliamButcherBot

$ cd WilliamButcherBot

$ pip3 install -U -r requirements.txt

$ cp sample_config.py config.py

$ rm .gitignore

$ heroku git:remote -a YOUR_HEROKU_APP_NAME

$ heroku stack:set container

$ git add -f .

$ git commit -m 'Hail WBB!'

$ git push heroku HEAD:master --force

$ heroku ps:scale worker=1
```


## Features 

* Group Management
* Music Downloading 
* AI Chatbot
* Web Scraping 
* Get Pictures/Wallpapers  
* Dictionary
* Translation
* Message Cryptography 
* Python Interpreter (Right In Your Telegram Chat!)
* Nekobin (Paste Code/Text)
* And Much More...
