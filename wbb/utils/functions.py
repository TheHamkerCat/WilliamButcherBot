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
from asyncio import gather
from datetime import datetime, timedelta
from io import BytesIO
from math import atan2, cos, radians, sin, sqrt
from os import execvp
from random import randint
from re import findall
from re import sub as re_sub
from sys import executable

import aiofiles
import speedtest
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from pyrogram.types import Message

from wbb import aiohttpsession as aiosession
from wbb.utils.dbfunctions import start_restart_stage
from wbb.utils.http import get, post


async def restart(m: Message):
    if m:
        await start_restart_stage(m.chat.id, m.message_id)
    execvp(executable, [executable, "-m", "wbb"])


def generate_captcha():
    # Generate one letter
    def gen_letter():
        return chr(randint(65, 90))

    def rndColor():
        return (randint(64, 255), randint(64, 255), randint(64, 255))

    def rndColor2():
        return (randint(32, 127), randint(32, 127), randint(32, 127))

    # Generate a 4 letter word
    def gen_wrong_answer():
        word = ""
        for _ in range(4):
            word += gen_letter()
        return word

    # Generate 8 wrong captcha answers
    wrong_answers = []
    for _ in range(8):
        wrong_answers.append(gen_wrong_answer())

    width = 80 * 4
    height = 100
    correct_answer = ""
    font = ImageFont.truetype("assets/arial.ttf", 55)
    file = f"assets/{randint(1000, 9999)}.jpg"
    image = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Draw random points on image
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=rndColor())

    for t in range(4):
        letter = gen_letter()
        correct_answer += letter
        draw.text((60 * t + 50, 15), letter, font=font, fill=rndColor2())
    image = image.filter(ImageFilter.BLUR)
    image.save(file, "jpeg")
    return [file, correct_answer, wrong_answers]


def test_speedtest():
    def speed_convert(size):
        power = 2 ** 10
        zero = 0
        units = {0: "", 1: "Kb/s", 2: "Mb/s", 3: "Gb/s", 4: "Tb/s"}
        while size > power:
            size /= power
            zero += 1
        return f"{round(size, 2)} {units[zero]}"

    speed = speedtest.Speedtest()
    info = speed.get_best_server()
    download = speed.download()
    upload = speed.upload()
    return [speed_convert(download), speed_convert(upload), info]


async def get_http_status_code(url: str) -> int:
    async with aiosession.head(url) as resp:
        return resp.status


async def make_carbon(code):
    url = "https://carbonara.vercel.app/api/cook"
    async with aiosession.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image


async def transfer_sh(file_or_message):
    if isinstance(file_or_message, Message):
        file_or_message = await file_or_message.download()
    file = file_or_message
    async with aiofiles.open(file, "rb") as f:
        params = {file: await f.read()}
        resp = await post("https://transfer.sh/", data=params)
        url = resp.strip()
    return url


async def calc_distance_from_ip(ip1: str, ip2: str) -> float:
    Radius_Earth = 6371.0088
    data1, data2 = await gather(
        get(f"http://ipinfo.io/{ip1}"),
        get(f"http://ipinfo.io/{ip2}"),
    )
    lat1, lon1 = data1["loc"].split(",")
    lat2, lon2 = data2["loc"].split(",")
    lat1, lon1 = radians(float(lat1)), radians(float(lon1))
    lat2, lon2 = radians(float(lat2)), radians(float(lon2))
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = Radius_Earth * c
    return distance


def get_urls_from_text(text: str) -> bool:
    regex = r"""(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]
                [.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(
                \([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\
                ()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))""".strip()
    return [x[0] for x in findall(regex, str(text))]


async def time_converter(message: Message, time_value: str) -> int:
    unit = ["m", "h", "d"]  # m == minutes | h == hours | d == days
    check_unit = "".join(list(filter(time_value[-1].lower().endswith, unit)))
    currunt_time = datetime.now()
    time_digit = time_value[:-1]
    if not time_digit.isdigit():
        return await message.reply_text("Incorrect time specified")
    if check_unit == "m":
        temp_time = currunt_time + timedelta(minutes=int(time_digit))
    elif check_unit == "h":
        temp_time = currunt_time + timedelta(hours=int(time_digit))
    elif check_unit == "d":
        temp_time = currunt_time + timedelta(days=int(time_digit))
    else:
        return await message.reply_text("Incorrect time specified.")
    return int(datetime.timestamp(temp_time))


async def extract_userid(message, text: str):
    """
    NOT TO BE USED OUTSIDE THIS FILE
    """

    def is_int(text: str):
        try:
            int(text)
        except ValueError:
            return False
        return True

    text = text.strip()

    if is_int(text):
        return int(text)

    entities = message.entities
    app = message._client
    if len(entities) < 2:
        return (await app.get_users(text)).id
    entity = entities[1]
    if entity.type == "mention":
        return (await app.get_users(text)).id
    if entity.type == "text_mention":
        return entity.user.id
    return None


async def extract_user_and_reason(message, sender_chat=False):
    args = message.text.strip().split()
    text = message.text
    user = None
    reason = None
    if message.reply_to_message:
        reply = message.reply_to_message
        # if reply to a message and no reason is given
        if not reply.from_user:
            if (
                reply.sender_chat
                and reply.sender_chat != message.chat.id
                and sender_chat
            ):
                id_ = reply.sender_chat.id
            else:
                return None, None
        else:
            id_ = reply.from_user.id

        if len(args) < 2:
            reason = None
        else:
            reason = text.split(None, 1)[1]
        return id_, reason

    # if not reply to a message and no reason is given
    if len(args) == 2:
        user = text.split(None, 1)[1]
        return await extract_userid(message, user), None

    # if reason is given
    if len(args) > 2:
        user, reason = text.split(None, 2)[1:]
        return await extract_userid(message, user), reason

    return user, reason


async def extract_user(message):
    return (await extract_user_and_reason(message))[0]


def get_file_id_from_message(
    message,
    max_file_size=3145728,
    mime_types=["image/png", "image/jpeg"],
):
    file_id = None
    if message.document:
        if int(message.document.file_size) > max_file_size:
            return

        mime_type = message.document.mime_type

        if mime_types and mime_type not in mime_types:
            return
        file_id = message.document.file_id

    if message.sticker:
        if message.sticker.is_animated:
            if not message.sticker.thumbs:
                return
            file_id = message.sticker.thumbs[0].file_id
        else:
            file_id = message.sticker.file_id

    if message.photo:
        file_id = message.photo.file_id

    if message.animation:
        if not message.animation.thumbs:
            return
        file_id = message.animation.thumbs[0].file_id

    if message.video:
        if not message.video.thumbs:
            return
        file_id = message.video.thumbs[0].file_id
    return file_id


def extract_text_and_keyb(ikb, text: str, row_width: int = 2):
    keyboard = {}
    try:
        text = text.strip()
        if text.startswith("`"):
            text = text[1:]
        if text.endswith("`"):
            text = text[:-1]

        text, keyb = text.split("~")

        keyb = findall(r"\[.+\,.+\]", keyb)
        for btn_str in keyb:
            btn_str = re_sub(r"[\[\]]", "", btn_str)
            btn_str = btn_str.split(",")
            btn_txt, btn_url = btn_str[0], btn_str[1].strip()

            if not get_urls_from_text(btn_url):
                continue
            keyboard[btn_txt] = btn_url
        keyboard = ikb(keyboard, row_width)
    except Exception:
        return
    return text, keyboard


async def get_user_id_and_usernames(client) -> dict:
    with client.storage.lock, client.storage.conn:
        users = client.storage.conn.execute(
            'SELECT * FROM peers WHERE type in ("user", "bot") AND username NOT null'
        ).fetchall()
    users_ = {}
    for user in users:
        users_[user[0]] = user[3]
    return users_
