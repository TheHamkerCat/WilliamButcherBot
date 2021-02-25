import requests as r
from pyrogram.types import Message
from pyrogram import filters
from wbb import app
from wbb.utils import cust_filter
from wbb.utils.errors import capture_err

__MODULE__ = "Succ"
__HELP__ = """/succ - Sends Succ Image For A Given Argument
/reddit [query] - results something from reddit"""

hack = [
    "https://i.ibb.co/YLLhCtt/i.png",
    "https://i.ibb.co/DMzyLMZ/e.jpg",
    "https://i.ibb.co/sqngHGt/d.jpg",
    "https://i.ibb.co/b1Y1rGf/a.jpg",
]

kemeest = "'https://i.ibb.co/bB4pqNN/i.jpg'"
educ = "'https://i.ibb.co/LCB3yTX/q.jpg'"
health = "'https://i.ibb.co/TKHxkH4/m.jpg'"
nhealth = "'https://i.ibb.co/dBVBzJY/p.jpg'"
feminism = "'https://i.ibb.co/PNhPJR1/o.jpg'"
security = "'https://i.ibb.co/ctf3MGM/c.jpg'"


def suck(text):
    socc = {
        "komidi": 'message.reply_photo("https://i.ibb.co/mRL3Nnf/j.jpg")',
        "kemist": f"message.reply_photo({kemeest})",
        "ejucation": f"message.reply_photo({educ})",
        "helth": f"message.reply_photo({health})",
        "nothelth": f"message.reply_photo({nhealth})",
        "femnnism": f"message.reply_photo({feminism})",
        "tehc": 'message.reply_photo("https://i.ibb.co/gdSvHSr/n.jpg")',
        "stonks": 'message.reply_photo("https://i.ibb.co/TtZ144x/h.png")',
        "sekuriti": f"message.reply_photo({security})",
        "phijiks": 'message.reply_photo("https://i.ibb.co/Zz4wBnc/g.png")',
        "welth": 'message.reply_photo("https://i.ibb.co/JxFm4pW/k.jpg")',
        "smrt": 'message.reply_photo("https://i.ibb.co/7bVkyC7/l.jpg")',
        "linuks": 'message.reply_photo("https://i.ibb.co/m6b0cB1/image.png")',
        "hacc": "message.reply_photo(random.choice(hack))",
    }
    return socc.get(text)


@app.on_message(cust_filter.command(commands=("succ")) & ~filters.edited)
@capture_err
def succ(_, message: Message):
    if len(message.command) != 2:
        message.reply_text(
            """"/succ" Needs And Argument
Args - `komidi, kemist, ejucation, helth, nothelth,
femnnism, tehc, hacc, stonks, sekuriti,
phijiks, welth, smrt`"""
        )
    result = suck(message.text.split(None, 1)[1])
    if result is None:
        message.reply_text(
            """"/succ" Needs And Argument
Args - `komidi, kemist, ejucation, helth, nothelth,
femnnism, tehc, hacc, stonks, sekuriti,
phijiks, welth, smrt`"""
        )
    exec(result)


@app.on_message(cust_filter.command(commands=("reddit")) & ~filters.edited)
@capture_err
async def reddit(_, message: Message):
    app.set_parse_mode("html")
    if len(message.command) != 2:
        await message.reply_text("/reddit needs an argument")
    subreddit = message.command[1]
    res = r.get(f"https://meme-api.herokuapp.com/gimme/{subreddit}")
    res = res.json()

    rpage = res.get(str("subreddit"))  # Subreddit
    title = res.get(str("title"))  # Post title
    memeu = res.get(str("url"))  # meme pic url
    plink = res.get(str("postLink"))

    caps = f"<b>Title</b>: {title}\n"
    caps += f"<b>Subreddit: </b>r/{rpage}\n"
    caps += f"<b>PostLink:</b> {plink}"
    await message.reply_photo(photo=memeu, caption=(caps))
