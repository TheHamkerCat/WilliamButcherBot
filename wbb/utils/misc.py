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
from math import ceil

from pyrogram.types import InlineKeyboardButton

from wbb import MOD_LOAD, MOD_NOLOAD


class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text


def paginate_modules(page_n, module_dict, prefix, chat=None):
    if not chat:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__MODULE__,
                    callback_data="{}_module({})".format(
                        prefix, x.__MODULE__.replace(" ", "_").lower()
                    ),
                )
                for x in module_dict.values()
            ]
        )
    else:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__MODULE__,
                    callback_data="{}_module({},{})".format(
                        prefix, chat, x.__MODULE__.replace(" ", "_").lower()
                    ),
                )
                for x in module_dict.values()
            ]
        )

    pairs = list(zip(modules[::3], modules[1::3], modules[2::3]))
    i = 0
    for m in pairs:
        for _ in m:
            i += 1
    if len(modules) - i == 1:
        pairs.append((modules[-1],))
    elif len(modules) - i == 2:
        pairs.append(
            (
                modules[-2],
                modules[-1],
            )
        )

    COLUMN_SIZE = 4

    max_num_pages = ceil(len(pairs) / COLUMN_SIZE)
    modulo_page = page_n % max_num_pages

    # can only have a certain amount of buttons side by side
    if len(pairs) > COLUMN_SIZE:
        pairs = pairs[
            modulo_page * COLUMN_SIZE : COLUMN_SIZE * (modulo_page + 1)
        ] + [
            (
                EqInlineKeyboardButton(
                    "❮",
                    callback_data="{}_prev({})".format(prefix, modulo_page),
                ),
                EqInlineKeyboardButton(
                    "Back",
                    callback_data="{}_home({})".format(prefix, modulo_page),
                ),
                EqInlineKeyboardButton(
                    "❯",
                    callback_data="{}_next({})".format(prefix, modulo_page),
                ),
            )
        ]

    return pairs


def is_module_loaded(name):
    return (not MOD_LOAD or name in MOD_LOAD) and name not in MOD_NOLOAD
