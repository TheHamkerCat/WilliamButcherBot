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

from asyncio import get_event_loop, sleep

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message

from wbb import app, arq
from wbb.core.keyboard import ikb

__MODULE__ = "Proxy"
__HELP__ = (
    "/proxy - Get socks5 proxy which you can"
    + " use with telegram or other things"
)

proxies = []


async def get_proxies():
    global proxies
    proxies = (await arq.proxy()).result


loop = get_event_loop()
loop.create_task(get_proxies())


def url_from_proxy(proxy: str) -> str:
    creds, proxy = proxy.split("//")[1:][0].split("@")
    user, passwd = creds.split(":")
    host, port = proxy.split(":")
    return (
        f"https://t.me/socks?server={host}&port="
        + f"{port}&user={user}&pass={passwd}"
    )


@app.on_message(filters.command("proxy") & ~filters.edited)
async def proxy_func(_, message: Message):
    if len(proxies) == 0:
        await sleep(0.5)
    location = proxies[0].location
    proxy = proxies[0].proxy
    url = url_from_proxy(proxy)
    keyb = ikb(
        {
            "←": "proxy_arq_-1",
            "→": "proxy_arq_1",
            "Connect": url,
        }
    )
    await message.reply_text(
        f"""
**Proxy:** {proxy}
**Location**: {location}

**POWERED BY [ARQ](http://t.me/ARQUpdates)**""",
        reply_markup=keyb,
        disable_web_page_preview=True,
    )


@app.on_callback_query(filters.regex(r"proxy_arq_"))
async def proxy_callback_func(_, cq: CallbackQuery):
    data = cq.data
    index = int(data.split("_")[-1])
    location = proxies[index].location
    proxy = proxies[index].proxy
    url = url_from_proxy(proxy)
    keyb = ikb(
        {
            "←": f"proxy_arq_{index-1}",
            "→": f"proxy_arq_{index+1}",
            "Connect": url,
        }
    )
    await cq.message.edit(
        f"""
**Proxy:** {proxy}
**Location**: {location}

**POWERED BY [ARQ](http://t.me/ARQUpdates)**""",
        reply_markup=keyb,
        disable_web_page_preview=True,
    )
