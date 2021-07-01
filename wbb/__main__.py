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
import asyncio
import importlib
import re
import random
import uvloop
from pyrogram import filters, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from wbb import (BOT_NAME, BOT_USERNAME, USERBOT_NAME, aiohttpsession,
                 app)
from wbb.modules import ALL_MODULES
from wbb.modules.sudoers import bot_sys_stats
from wbb.utils import paginate_modules
from wbb.utils.dbfunctions import clean_restart_stage

loop = asyncio.get_event_loop()

HELPABLE = {}


async def start_bot():
    restart_data = await clean_restart_stage()
    if restart_data:
        print("[INFO]: SENDING RESTART STATUS")
        try:
            await app.edit_message_text(
                restart_data["chat_id"],
                restart_data["message_id"],
                "**Restarted Successfully**",
            )
        except Exception:
            pass
    for module in ALL_MODULES:
        imported_module = importlib.import_module(
            "wbb.modules." + module
        )
        if (
            hasattr(imported_module, "__MODULE__")
            and imported_module.__MODULE__
        ):
            imported_module.__MODULE__ = imported_module.__MODULE__
            if (
                hasattr(imported_module, "__HELP__")
                and imported_module.__HELP__
            ):
                HELPABLE[
                    imported_module.__MODULE__.lower()
                ] = imported_module
    bot_modules = ""
    j = 1
    for i in ALL_MODULES:
        if j == 4:
            bot_modules += "|{:<15}|\n".format(i)
            j = 0
        else:
            bot_modules += "|{:<15}".format(i)
        j += 1
    print(
        "+===============================================================+"
    )
    print(
        "|                              ODA                              |"
    )
    print(
        "+===============+===============+===============+===============+"
    )
    print(bot_modules)
    print(
        "+===============+===============+===============+===============+"
    )
    print(f"[INFO]: BOT STARTED AS {BOT_NAME}!")
    print(f"[INFO]: USERBOT STARTED AS {USERBOT_NAME}!")
    await idle()
    print("[INFO]: STOPPING BOT AND CLOSING AIOHTTP SESSION")
    await aiohttpsession.close()


@app.on_message(filters.command(["help", "start"]))
async def help_command(_, message):
    if message.chat.type != "private":
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="[► Help ◄]",
                        url=f"t.me/{BOT_USERNAME}?start=help",
                    ),
                    InlineKeyboardButton(
                        text="✫ Source Code ✫",
                        url="https://UserLazy.github.io/UserLazy",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="System Stats ",
                        callback_data="stats_callback",
                    ),
                    InlineKeyboardButton(
                        text="✯ Anime Group ✯", url="t.me/Grup_Anime_Chat"
                    ),
                ],
            ]
        )
        await message.reply(
            "Pm Me For More Details.", reply_markup=keyboard
        )
        return
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="[► Help ◄]", callback_data="bot_commands"
                ),
                InlineKeyboardButton(
                    text="✯ Support Group ✯",
                    url="https://t.me/OdaSupport",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="System Stats ",
                    callback_data="stats_callback",
                ),
                InlineKeyboardButton(
                    text="✯ Anime Group ✯", url="t.me/Grup_Anime_Chat"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="✤ Add to your Group ✤",
                    url=f"http://t.me/{BOT_USERNAME}?startgroup=new",
                )
            ],
        ]
    )
    STICKERS = (
    "CAACAgEAAxkDAAEE5zBgzpDoaKGN_MxWotYtWkpb1ifgMgACXAADni6oMXCx-PB6sonJHgQ",
    "CAACAgEAAxkDAAEE5zFgzpFDFp_0V9vi-r5ZnKaOUDCVkAACVQADni6oMROiUdEEyPN8HgQ",
    "CAACAgEAAxkDAAEE5zJgzpFxlslQcP9Xdjsvqb2oqkZrxQACeAADni6oMQhcS_oH6wPjHgQ",
    "CAACAgEAAxkDAAEE5zNgzpGbRbc_ecGW1qIk2qojT0yTmgACdwADni6oMd2k3jP94wO6HgQ",
    "CAACAgEAAxkDAAEE5zZgzpG9wHOrBm-X_gNGWlUSGXkEMQACWAADni6oMe7FeddXzDLoHgQ",
    "CAACAgUAAx0CRI6ivgAC1qVg2iEgaRvIKr9auH4VGEalNK8UGAACAQMAAvEAAdBWNmr7bsO-rvseBA",
    "CAACAgUAAx0CRI6ivgAC1rFg2iIT1mcmXTV1TZvM2WaA0tmKuAACRAMAAmpP0Fb1Txeqb6b0AR4E",
    "CAACAgUAAx0CRI6ivgAC1rpg2iJ0UnLFLvWLw86DTatSLyKnvgAChwMAAlf90VYju1kc0R0pdB4E",
    "CAACAgUAAx0CRI6ivgAC1sJg2iLnlFEKWs07Jw-ws784R01FTwACrQIAAlhx0FaXbV8XMcrAWx4E",
    "CAACAgUAAx0CRI6ivgAC1sxg2iNwFjooHU0PjKL48FdVRw_NIwACyAMAAoyf0FaMuLOiawABEEceBA",
    "CAACAgUAAx0CRI6ivgAC1tRg2iPn9I5BtWpa_dL0kq7b4qvd-AAC-QIAArxX0VbSgHcf_OyMMB4E",
)
    await message.reply_sticker(random.choice(STICKERS))
    await message.reply(
        f"Hey there! My name is {BOT_NAME}. I can manage your group with lots of useful features, feel free to add me to your group.",
        reply_markup=keyboard,
    )


async def help_parser(name, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(
            paginate_modules(0, HELPABLE, "help")
        )
    return (
        """Main commands available[:](https://telegra.ph/file/3c0e87516360f7343668b.jpg)
 ➛ /start: check my Alive in your PM!
 ➛ /help <module name>: PM's you info about that module.
 ➛ /repo: fo get source code
 ➛ /help:
   ❂ in PM: will send you your settings for all supported modules.
   ❂ in a group: will redirect you to pm, with all that chat's settings.""".format(
            first_name=name,
            bot_name=BOT_NAME,
        ),
        keyboard,
    )


@app.on_callback_query(filters.regex("bot_commands"))
async def commands_callbacc(_, CallbackQuery):
    text, keyboard = await help_parser(
        CallbackQuery.from_user.mention
    )
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=text,
        reply_markup=keyboard,
    )

    await CallbackQuery.message.delete()


@app.on_callback_query(filters.regex("stats_callback"))
async def stats_callbacc(_, CallbackQuery):
    text = await bot_sys_stats()
    await app.answer_callback_query(
        CallbackQuery.id, text, show_alert=True
    )


@app.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(client, query):
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    create_match = re.match(r"help_create", query.data)
    top_text = f"""
Hello {query.from_user.first_name}! My name is {BOT_NAME}!
I'm a group management bot with some usefule features.
═════════════════════════════
Maintained By @RxyMX
═════════════════════════════
Main commands available[:](https://telegra.ph/file/3c0e87516360f7343668b.jpg)
 ➛ /start: check my Alive in your PM!
 ➛ /help <module name>: PM's you info about that module.
 ➛ /repo: fo get source code
 ➛ /help:
   ❂ in PM: will send you your settings for all supported modules.
   ❂ in a group: will redirect you to pm, with all that chat's settings.
 """
    if mod_match:
        module = mod_match.group(1)
        text = (
            "{} **{}**:\n".format(
                "Here is the help for", HELPABLE[module].__MODULE__
            )
            + HELPABLE[module].__HELP__
        )

        await query.message.edit(
            text=text,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "back", callback_data="help_back"
                    ),
                    InlineKeyboardButton(
                        text="✫ OdaXMusic Repo ✫",
                        url="https://github.con/UserLazy/Oda_Music",
                        )
                    ]
                ]
            ),
            disable_web_page_preview=True,
        )

    elif prev_match:
        curr_page = int(prev_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(curr_page - 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif next_match:
        next_page = int(next_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(next_page + 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif back_match:
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(0, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif create_match:
        text, keyboard = await help_parser(query)
        await query.message.edit(
            text=text,
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )

    return await client.answer_callback_query(query.id)


if __name__ == "__main__":
    uvloop.install()
    loop.run_until_complete(start_bot())
