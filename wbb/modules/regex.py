# https://github.com/PaulSonOfLars/tgbot/blob/master/tg_bot/modules/sed.py
from re import I
from re import search as re_search
from re import sub as re_sub
from sre_constants import error as sre_error

from pyrogram import filters
from wbb import app
from wbb.utils.filter_groups import regex_group

__MODULE__ = "Sed"
__HELP__ = "**Usage:**\ns/foo/bar"

DELIMITERS = ("/", ":", "|", "_")


@app.on_message(
    filters.regex(r"s([{}]).*?\1.*".format("".join(DELIMITERS))),
    group=regex_group,
)
async def sed(_, message):
    if not message.text:
        return
    sed_result = separate_sed(message.text)
    if message.reply_to_message:
        if message.reply_to_message.text:
            to_fix = message.reply_to_message.text
        elif message.reply_to_message.caption:
            to_fix = message.reply_to_message.caption
        else:
            return
        try:
            repl, repl_with, flags = sed_result
        except Exception:
            return

        if not repl:
            return await message.reply_text(
                "You're trying to replace... " "nothing with something?"
            )

        try:

            if infinite_checker(repl):
                return await message.reply_text("Nice try -_-")

            if "i" in flags and "g" in flags:
                text = re_sub(repl, repl_with, to_fix, flags=I).strip()
            elif "i" in flags:
                text = re_sub(
                    repl, repl_with, to_fix, count=1, flags=I
                ).strip()
            elif "g" in flags:
                text = re_sub(repl, repl_with, to_fix).strip()
            else:
                text = re_sub(repl, repl_with, to_fix, count=1).strip()
        except sre_error:
            return

        # empty string errors -_-
        if len(text) >= 4096:
            await message.reply_text(
                "The result of the sed command was too long for \
                                                 telegram!"
            )
        elif text:
            await message.reply_to_message.reply_text(text)


def infinite_checker(repl):
    regex = [
        r"\((.{1,}[\+\*]){1,}\)[\+\*].",
        r"[\(\[].{1,}\{\d(,)?\}[\)\]]\{\d(,)?\}",
        r"\(.{1,}\)\{.{1,}(,)?\}\(.*\)(\+|\* |\{.*\})",
    ]
    for match in regex:
        status = re_search(match, repl)
        return bool(status)


def separate_sed(sed_string):
    if len(sed_string) < 3 or sed_string[1] not in DELIMITERS or sed_string.count(sed_string[1]) < 2:
        return
    delim = sed_string[1]
    start = counter = 2
    while counter < len(sed_string):
        if sed_string[counter] == "\\":
            counter += 1
        elif sed_string[counter] == delim:
            replace = sed_string[start:counter]
            counter += 1
            start = counter
            break
        counter += 1
    else:
        return None
    while counter < len(sed_string):
        if (
                sed_string[counter] == "\\"
                and counter + 1 < len(sed_string)
                and sed_string[counter + 1] == delim
        ):
            sed_string = sed_string[:counter] + sed_string[counter + 1:]

        elif sed_string[counter] == delim:
            replace_with = sed_string[start:counter]
            counter += 1
            break
        counter += 1
    else:
        return replace, sed_string[start:], ""
    flags = sed_string[counter:] if counter < len(sed_string) else ""
    return replace, replace_with, flags.lower()
