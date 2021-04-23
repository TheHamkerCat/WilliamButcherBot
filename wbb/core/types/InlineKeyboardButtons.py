"""Written By github.com/Pokurt"""

from pyrogram.types import InlineKeyboardButton
import re

matching = r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"


def InlineKeyboardButtonDict(response: dict):
    temp = []
    for name, value in response.items():
        if re.findall(matching, value):
            temp.append(InlineKeyboardButton(name, url=value))
        else:
            temp.append(InlineKeyboardButton(name, callback_data=value))
    return temp
