# WilliamButcherBot
Just Another Telegram Bot Written In Python Using Pyrogram.

<img src="https://i.ibb.co/5WvFvLy/trevor-barclay-butcher2.jpg" width="160" align="right">

## Requirements

- Python 3.6 or higher.
- A [Telegram API key](//docs.pyrogram.org/intro/setup#api-keys).
- A [Telegram bot token](//t.me/botfather).

## Run

1. `git clone https://github.com/thehamkercat/WilliamButcherBot`, to download the source code.
2. `cd wbb`, to enter the directory.
3. `pip3 install -r requirements.txt`, to install the requirements.
4. `cp sample_config.ini config.ini` It should look like the code below:<br>

```
   [pyrogram]
   api_id = 12345
   api_hash = 0123456789abcdef0123456789abcdef
   bot_token = 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
   
   [admin]
   owner_id = 1243703097

   [prefix]
   prefixes = /

   [mods]
   load_modules =
   noload_modules =
   ```
5. Run with `python3 -m wbb`

## License

MIT © 2019-2020
