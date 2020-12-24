import random
from pyrogram.types import Message
from wbb import app
from wbb.utils import cust_filter
from pyrogram import filters

__MODULE__ = "Succ"
__HELP__ = "/succ - Sends Succ Image For A Given Argument"

edu = "https://i.ibb.co/LCB3yTX/q.jpg"
nothealth = "https://i.ibb.co/dBVBzJY/p.jpg"
health = "https://i.ibb.co/TKHxkH4/m.jpg"
feminists = "https://i.ibb.co/PNhPJR1/o.jpg"
tech = "https://i.ibb.co/gdSvHSr/n.jpg"
smart = "https://i.ibb.co/7bVkyC7/l.jpg"
wealth = "https://i.ibb.co/JxFm4pW/k.jpg"
hack = ['https://i.ibb.co/YLLhCtt/i.png', 'https://i.ibb.co/DMzyLMZ/e.jpg',
        'https://i.ibb.co/sqngHGt/d.jpg', 'https://i.ibb.co/b1Y1rGf/a.jpg']
comedy = "https://i.ibb.co/mRL3Nnf/j.jpg"
chemist = "https://i.ibb.co/bB4pqNN/i.jpg"
stonks = "https://i.ibb.co/TtZ144x/h.png"
physics = "https://i.ibb.co/Zz4wBnc/g.png"
security = "https://i.ibb.co/ctf3MGM/c.jpg"
engineer = "https://i.ibb.co/8DP8LBx/b.jpg"


@app.on_message(cust_filter.command(commands=("succ")) & ~filters.edited)
async def succ(_, message: Message):
    text = message.text.replace('/succ ', '')
    app.set_parse_mode("markdown")
    if text == 'komidi':
        await message.reply_photo(comedy)
    if text == 'kemist':
        await message.reply_photo(chemist)
    if text == 'ejucation':
        await message.reply_photo(edu)
    if text == 'helth':
        await message.reply_photo(health)
    if text == 'nothelth':
        await message.reply_photo(nothealth)
    if text == 'femnnism':
        await message.reply_photo(feminists)
    if text == 'tehc':
        await message.reply_photo(tech)
    if text == 'stonks':
        await message.reply_photo(stonks)
    if text == 'sekuriti':
        await message.reply_photo(security)
    if text == 'enjenir':
        await message.reply_photo(engineer)
    if text == 'phijiks':
        await message.reply_photo(physics)
    if text == 'welth':
        await message.reply_photo(wealth)
    if text == 'smrt':
        await message.reply_photo(smart)
    if text == 'hacc':
        await message.reply_photo(random.choice(hack))
    elif text == '/succ':
        await message.reply_text('''
"/succ" Needs And Argument
Args - `komidi, kemist, ejucation, helth, nothelth,
femnnism, tehc, hacc, stonks, sekuriti, enjenir,
phijiks, welth, smrt`''')
