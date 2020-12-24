import random
from pyrogram.types import Message
from pyrogram import filters
from wbb import app
from wbb.utils import cust_filter

__MODULE__ = "Succ"
__HELP__ = "/succ - Sends Succ Image For A Given Argument"

hack = ['https://i.ibb.co/YLLhCtt/i.png', 'https://i.ibb.co/DMzyLMZ/e.jpg',
        'https://i.ibb.co/sqngHGt/d.jpg', 'https://i.ibb.co/b1Y1rGf/a.jpg']

kemeest = "'https://i.ibb.co/bB4pqNN/i.jpg'"
educ = "'https://i.ibb.co/LCB3yTX/q.jpg'"
health = "'https://i.ibb.co/TKHxkH4/m.jpg'"
nhealth = "'https://i.ibb.co/dBVBzJY/p.jpg'"
feminism = "'https://i.ibb.co/PNhPJR1/o.jpg'"
security = "'https://i.ibb.co/ctf3MGM/c.jpg'"


def suck(text):
    socc = {'komidi': 'message.reply_photo("https://i.ibb.co/mRL3Nnf/j.jpg")',
            'kemist': f'message.reply_photo({kemeest})',
            'ejucation': f'message.reply_photo({educ})',
            'helth': f'message.reply_photo({health})',
            'nothelth': f'message.reply_photo({nhealth})',
            'femnnism': f'message.reply_photo({feminism})',
            'tehc': 'message.reply_photo("https://i.ibb.co/gdSvHSr/n.jpg")',
            'stonks': 'message.reply_photo("https://i.ibb.co/TtZ144x/h.png")',
            'sekuriti': 'message.reply_photo()',
            'enjenir': f'message.reply_photo({security})',
            'phijiks': 'message.reply_photo("https://i.ibb.co/Zz4wBnc/g.png")',
            'welth': 'message.reply_photo("https://i.ibb.co/JxFm4pW/k.jpg")',
            'smrt': 'message.reply_photo("https://i.ibb.co/7bVkyC7/l.jpg")',
            'hacc': 'message.reply_photo(random.choice(hack))'}
    return socc.get(text)


@app.on_message(cust_filter.command(commands=("succ")) & ~filters.edited)
def succ(_, message: Message):
    result = suck(message.text.replace('/succ ', ''))
    print(result)
    if result is None:
        message.reply_text('''"/succ" Needs And Argument
Args - `komidi, kemist, ejucation, helth, nothelth,
femnnism, tehc, hacc, stonks, sekuriti, enjenir,
phijiks, welth, smrt`''')
    print(random)
    exec(result)
