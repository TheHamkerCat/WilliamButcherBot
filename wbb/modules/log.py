from pyrogram import filters, types
import re
from wbb.utils import cust_filter, nekobin
from wbb import app, OWNER_ID


__MODULE__ = "Logs"
__HELP__ = "/log - To Get Logs From Last Run [Owner Only]"

@app.on_message(filters.user(OWNER_ID) & cust_filter.command("log"))
async def logs_chat(client, message):
    keyb = types.InlineKeyboardMarkup(
        [
            [
                types.InlineKeyboardButton(
                    "Paste on Nekobin", callback_data="paste_log_nekobin"
                )
            ]
        ]
    )
    await message.reply_document(
        "wbb/logs/error.log", caption="✨ **Here are my Logs ~**", reply_markup=keyb
    )


def logs_callback(_, __, query):
    if re.match("paste_log_nekobin", query.data):
        return True


logs_create = filters.create(logs_callback)


@app.on_callback_query(logs_create)
async def paste_log_neko(client, query):
    if query.from_user.id == OWNER_ID:
        f = open("wbb/logs/error.log", "r")
        data = await nekobin.neko(f.read())
        keyb = types.InlineKeyboardMarkup(
            [[types.InlineKeyboardButton("pasted on nekobin", url=f"{data}")]]
        )
        await query.message.edit_caption("Successfully Nekofied", reply_markup=keyb)
    else:
        await client.answer_callback_query(
            query.id, "'Blue Button Must Press', huh?", show_alert=True
        )
