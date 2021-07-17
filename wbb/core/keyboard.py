"""
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
"""
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from wbb.utils.functions import get_urls_from_text


def btn(text, data, type=None):
    type = "url" if get_urls_from_text(data) else "callback_data"
    return InlineKeyboardButton(text, **{type: data})


def ikb(keyboard: list):
    lines = []
    for row in keyboard:
        line = []
        for button in row:
            button = btn(*button)  # InlineKeyboardButton
            line.append(button)
        lines.append(line)
    return InlineKeyboardMarkup(inline_keyboard=lines)


def build_button(buttons: list):
        if not buttons:
            return None
        keyboard = []
        for button in buttons:
            if button[2] and keyboard:
                keyboard[-1].append(InlineKeyboardButton(button[0], url=button[1]))
            else:
                keyboard.append([InlineKeyboardButton(button[0], url=button[1])])
        return InlineKeyboardMarkup(keyboard)


def revert_button(button: list):
        res = ""
        for btn in button:
            if btn[2]:
                res += f"\n[{btn[0]}, {btn[1]}, 2]"
            else:
                res += f"\n[{btn[0]}, {btn[1]}]"
        return res

