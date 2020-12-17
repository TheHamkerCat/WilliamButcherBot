import asyncio
import re
from pyrogram import filters, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from wbb import app, MOD_NOLOAD, MOD_LOAD, Command
from wbb.utils import random_line, get_info, paginate_modules, cust_filter
import importlib
from wbb.modules import ALL_MODULES
import uvloop

loop = asyncio.get_event_loop()


HELPABLE = {}


async def start_bot():
    await app.start()
    await get_info(app)
    from wbb.utils import botinfo

    await main_bot()
    for modul in ALL_MODULES:
        imported_module = importlib.import_module("wbb.modules." + modul)
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            if imported_module.__MODULE__.lower() in MOD_NOLOAD:
                continue
            imported_module.__MODULE__ = imported_module.__MODULE__
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                HELPABLE[imported_module.__MODULE__.lower()] = imported_module
    bot_modules = ""
    j = 1
    for i in ALL_MODULES:
        if j == 4:
            bot_modules += "|{:<15}|\n".format(i)
            j = 0
        else:
            bot_modules += "|{:<15}".format(i)
        j += 1
    print("+===============================================================+")
    print("|                         WBB - Modules                         |")
    print("+===============+===============+===============+===============+")
    print(bot_modules)
    print("+===============+===============+===============+===============+")
    print("Bot Started Successfully as {}!".format(botinfo.BOT_NAME))
    await idle()


async def main_bot():
    from wbb.utils import botinfo

    @app.on_message(cust_filter.command("start"))
    async def start(client, message):
        if message.chat.type != "private":
            await message.reply_text((await random_line("wbb/utils/start.txt")))
            return
        await message.reply("Hi, try /help")

    @app.on_message(cust_filter.command("help"))
    async def help_command(_, message):
        if message.chat.type != "private":
            if len(message.command) >= 2 and message.command[1] == "help":
                text, keyboard = await help_parser(message)
                await message.reply(
                    text, reply_markup=keyboard, disable_web_page_preview=True
                )
                return
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Help",
                            url="t.me/" + botinfo.BOT_USERNAME + "?start=help",
                        )
                    ]
                ]
            )
            await message.reply("Contact me in PM.", reply_markup=keyboard)
            return
        text, keyboard = await help_parser(message)
        await message.reply(text, reply_markup=keyboard, disable_web_page_preview=True)

    async def help_parser(message, keyboard=None):
        if not keyboard:
            keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
        return (
            "Hi {first_name}, I am {bot_name}".format(
                first_name=message.from_user.first_name,
                bot_name=botinfo.BOT_NAME,
                commands=", ".join(Command),
            ),
            keyboard,
        )

    @app.on_callback_query(filters.regex(r"help_(.*?)"))
    async def help_button(c, q):
        mod_match = re.match(r"help_module\((.+?)\)", q.data)
        prev_match = re.match(r"help_prev\((.+?)\)", q.data)
        next_match = re.match(r"help_next\((.+?)\)", q.data)
        back_match = re.match(r"help_back", q.data)
        create_match = re.match(r"help_create", q.data)

        if mod_match:
            module = mod_match.group(1)
            text = (
                "{} **{}**:\n".format(
                    "Here is the help for", HELPABLE[module].__MODULE__
                )
                + HELPABLE[module].__HELP__
            )

            await q.message.edit(
                text=text,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("back", callback_data="help_back")]]
                ),
                disable_web_page_preview=True,
            )

        elif prev_match:
            curr_page = int(prev_match.group(1))
            await q.message.edit(
                text="Hi {first_name}. I am {bot_name}, you can use commands with following prefixes{commands}".format(
                    first_name=q.from_user.first_name,
                    bot_name=botinfo.BOT_NAME,
                    commands=", ".join(Command),
                ),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, HELPABLE, "help")
                ),
                disable_web_page_preview=True,
            )

        elif next_match:
            next_page = int(next_match.group(1))
            await q.message.edit(
                text="Hi {first_name}. I am {bot_name}, you can use commands with following prefixes{commands}".format(
                    first_name=q.from_user.first_name,
                    bot_name=botinfo.BOT_NAME,
                    commands=", ".join(Command),
                ),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, HELPABLE, "help")
                ),
                disable_web_page_preview=True,
            )

        elif back_match:
            await q.message.edit(
                text="Hi {first_name}. I am {bot_name}, you can use commands with following prefixes{commands}".format(
                    first_name=q.from_user.first_name,
                    bot_name=botinfo.BOT_NAME,
                    commands=", ".join(Command),
                ),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELPABLE, "help")
                ),
                disable_web_page_preview=True,
            )

        elif create_match:
            text, keyboard = await help_parser(q)
            await q.message.edit(
                text=text, reply_markup=keyboard, disable_web_page_preview=True
            )

        return await c.answer_callback_query(q.id)


if __name__ == "__main__":
    uvloop.install()
    loop.run_until_complete(start_bot())
