import itertools
import os
import random
import secrets
from textwrap import TextWrapper
from urllib.request import urlretrieve

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from .crop import crop_to_circle
from .get_height import get_y_and_heights
from .rectangle import rounded_rectangle

""" Taken From https://github.com/pokurt/Nana-Remix/tree/
8d10285c9ba68ec127d3d4f0d6e7a67e48ca5f4d/nana/utils/sticker """


COLORS = [
    '#F07975',
    '#F49F69',
    '#F9C84A',
    '#8CC56E',
    '#6CC7DC',
    '#80C1FA',
    '#BCB3F9',
    '#E181AC',
]

urlretrieve(
    'https://github.com/pokurt/Fonts/raw/master/NotoSansDisplay-Bold.ttf',
    'wbb/modules/sticker/NotoSansDisplay-Bold.ttf',
)

urlretrieve(
    'https://github.com/pokurt/Fonts/raw/master/OpenSans-Regular.ttf',
    'wbb/modules/sticker/OpenSans-Regular.ttf',
)


async def create_sticker(client, message):
    if len(message.text) < 100:
        body_font_size = 25
        wrap_size = 40
    elif len(message.text) < 200:
        body_font_size = 20
        wrap_size = 45
    elif len(message.text) < 500:
        body_font_size = 17
        wrap_size = 50
    elif len(message.text) < 1000:
        body_font_size = 15
        wrap_size = 90
    else:
        body_font_size = 8
        wrap_size = 200

    font = ImageFont.truetype(
        'wbb/modules/sticker/OpenSans-Regular.ttf',
        body_font_size,
    )
    font_who = ImageFont.truetype(
        'wbb/modules/sticker/NotoSansDisplay-Bold.ttf',
        24,
    )

    img = Image.new(
        'RGBA',
        (512, 512),
        (255, 255, 255, 0),
    )
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle = rounded_rectangle

    wrapper = TextWrapper(
        width=wrap_size,
        break_long_words=False,
        replace_whitespace=False,
    )
    lines_list = [
        wrapper.wrap(i) for i in message.text.split('\n') if i != ''
    ]
    text_lines = list(itertools.chain.from_iterable(lines_list))

    y, line_heights = await get_y_and_heights(
        text_lines,
        (512, 512),
        10,
        font,
    )

    in_y = y
    rec_y = (y + line_heights[0]) if wrap_size >= 40 else y

    for i, _ in enumerate(text_lines):
        rec_y += line_heights[i]

    await rounded_rectangle(
        draw,
        (
            (90, in_y),
            (512, rec_y + line_heights[-1]),
        ),
        10,
        fill='#e0e0e0',
    )
    first = message.from_user.first_name
    f_user = (
        first
        + ' '
        + message.from_user.last_name
        if message.from_user.last_name else first
    )
    draw.text(
        (100, y),
        f'{f_user}',
        random.choice(COLORS),
        font=font_who,
    )

    y = (y + (line_heights[0] * (20/100))) if wrap_size >= 40 else y

    x = 100
    for i, line in enumerate(text_lines):
        y += line_heights[i]
        draw.text((x, y), line, '#211536', font=font)

    try:
        user_profile_pic = await client.get_profile_photos(
            message.from_user.id,
        )
        photo = await client.download_media(user_profile_pic[0].file_id)
    except IndexError:
        urlretrieve(
            'https://telegra.ph/file/1d3bf9a37547be4b04dcd.jpg',
            'wbb/modules/sticker/default.jpg',
        )
        photo = 'wbb/modules/sticker/default.jpg'

    im = Image.open(photo).convert('RGBA')
    im.thumbnail((60, 60))
    await crop_to_circle(im)
    img.paste(im, (20, in_y))

    sticker_file = f'{secrets.token_hex(2)}.webp'

    img.save(sticker_file)

    await message.reply_sticker(
        sticker=sticker_file,
    )

    if os.path.isfile(sticker_file):
        os.remove(sticker_file)
