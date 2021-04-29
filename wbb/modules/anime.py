# Part of Pull Req #2 by @MaskedVirus | github.com/swatv3nub

import os
import html
import math
import time
import requests
import json
import asyncio
import tempfile
from decimal import Decimal
from datetime import timedelta
from urllib.parse import quote as urlencode
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from wbb import app, telegraph, session
from wbb.core.decorators.errors import capture_err

__MODULE__ = "Anime"
__HELP__ = "•Anime uwu•\n\n/anime - search anime on AniList\n /manga - search manga on Anilist\n /char - search character on Anilist\n /wa by replying to a media - find what anime a media is from\n /nhentai ID - returns the nhentai in telegraph instant preview format."

def shorten(description, info='anilist.co'):
    ms_g = ""
    if len(description) > 700:
        description = description[0:500] + '....'
        ms_g += f"\n**Description**: __{description}__[More here]({info})"
    else:
        ms_g += f"\n**Description**: __{description}__"
    return (
        ms_g.replace("<br>", "")
        .replace("</br>", "")
        .replace("<i>", "")
        .replace("</i>", "")
    )


def t(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + " Days, ") if days else "") + \
        ((str(hours) + " Hours, ") if hours else "") + \
        ((str(minutes) + " Minutes, ") if minutes else "") + \
        ((str(seconds) + " Seconds, ") if seconds else "") + \
        ((str(milliseconds) + " ms, ") if milliseconds else "")
    return tmp[:-2]


airing_query = '''
    query ($id: Int,$search: String) { 
      Media (id: $id, type: ANIME,search: $search) { 
        id
        episodes
        title {
          romaji
          english
          native
        }
        siteUrl
        nextAiringEpisode {
           airingAt
           timeUntilAiring
           episode
        } 
      }
    }
    '''

fav_query = """
query ($id: Int) { 
      Media (id: $id, type: ANIME) { 
        id
        title {
          romaji
          english
          native
        }
     }
}
"""

anime_query = '''
   query ($id: Int,$search: String) { 
      Media (id: $id, type: ANIME,search: $search) { 
        id
        idMal
        title {
          romaji
          english
          native
        }
        description (asHtml: false)
        startDate{
            year
          }
          episodes
          season
          type
          format
          status
          duration
          siteUrl
          studios{
              nodes{
                   name
              }
          }
          trailer{
               id
               site 
               thumbnail
          }
          averageScore
          genres
          bannerImage
      }
    }
'''
character_query = """
    query ($query: String) {
        Character (search: $query) {
               id
               name {
                     first
                     last
                     full
               }
               siteUrl
               favourites
               image {
                        large
               }
               description
        }
    }
"""

manga_query = """
query ($id: Int,$search: String) { 
      Media (id: $id, type: MANGA,search: $search) { 
        id
        title {
          romaji
          english
          native
        }
        description (asHtml: false)
        startDate{
            year
          }
          type
          format
          status
          siteUrl
          averageScore
          genres
          bannerImage
      }
    }
"""

def format_bytes(size):
    size = int(size)
    power = 1024
    n = 0
    power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return f"{size:.2f} {power_labels[n]+'B'}"


def return_progress_string(current, total):
    filled_length = int(30 * current // total)
    return '[' + '=' * filled_length + ' ' * (30 - filled_length) + ']'


def calculate_eta(current, total, start_time):
    if not current:
        return '00:00:00'
    end_time = time.time()
    elapsed_time = end_time - start_time
    seconds = (elapsed_time * (total / current)) - elapsed_time
    thing = ''.join(str(timedelta(seconds=seconds)).split('.')[:-1]).split(', ')
    thing[-1] = thing[-1].rjust(8, '0')
    return ', '.join(thing)


url = 'https://graphql.anilist.co'


@app.on_message(filters.command("anime"))
@capture_err
async def anime_search(_, message):
    search = message.text.split(' ', 1)
    if len(search) == 1:
        await message.delete()
        return
    else:
        search = search[1]
    variables = {'search': search}
    json = requests.post(url, json={'query': anime_query, 'variables': variables}).json()[
        'data'].get('Media', None)
    if json:
        msg = f"**{json['title']['romaji']}**(`{json['title']['native']}`)\n**Type**: {json['format']}\n**Status**: {json['status']}\n**Episodes**: {json.get('episodes', 'N/A')}\n**Duration**: {json.get('duration', 'N/A')} Per Ep.\n**Score**: {json['averageScore']}\n**Genres**: `"
        for x in json['genres']:
            msg += f"{x}, "
        msg = msg[:-2] + '`\n'
        msg += "**Studios**: `"
        for x in json['studios']['nodes']:
            msg += f"{x['name']}, "
        msg = msg[:-2] + '`\n'
        info = json.get('siteUrl')
        trailer = json.get('trailer', None)
        if trailer:
            trailer_id = trailer.get('id', None)
            site = trailer.get('site', None)
            if site == "youtube":
                trailer = 'https://youtu.be/' + trailer_id
        description = json.get(
            'description', 'N/A').replace('<i>', '').replace('</i>', '').replace('<br>', '')
        msg += shorten(description, info)
        image = info.replace('anilist.co/anime/', 'img.anili.st/media/')
        if trailer:
            buttons = [
                    [InlineKeyboardButton("More Info", url=info),
                    InlineKeyboardButton("Trailer", url=trailer)]
                    ]
        else:
            buttons = [
                    [InlineKeyboardButton("More Info", url=info)]
                    ]
        if image:
            try:
                await message.reply_photo(image, caption=msg, reply_markup=InlineKeyboardMarkup(buttons))
            except:
                msg += f" [✔️️]({image})"
                await message.edit(msg)
        else:
            await message.edit(msg)


@app.on_message(filters.command("manga"))
@capture_err
async def manga_search(_, message):
    search = message.text.split(' ', 1)
    if len(search) == 1:
        await message.delete()
        return
    search = search[1]
    variables = {'search': search}
    json = requests.post(url, json={'query': manga_query, 'variables': variables}).json()[
        'data'].get('Media', None)
    ms_g = ''
    if json:
        title, title_native = json['title'].get(
            'romaji', False), json['title'].get('native', False)
        start_date, status, score = json['startDate'].get('year', False), json.get(
            'status', False), json.get('averageScore', False)
        if title:
            ms_g += f"**{title}**"
            if title_native:
                ms_g += f"(`{title_native}`)"
        if start_date:
            ms_g += f"\n**Start Date** - `{start_date}`"
        if status:
            ms_g += f"\n**Status** - `{status}`"
        if score:
            ms_g += f"\n**Score** - `{score}`"
        ms_g += '\n**Genres** - '
        for x in json.get('genres', []):
            ms_g += f"{x}, "
        ms_g = ms_g[:-2]

        image = json.get("bannerImage", False)
        ms_g += f"_{json.get('description', None)}_"
        if image:
            try:
                await message.reply_photo(image, caption=ms_g)
            except:
                ms_g += f" [✔️️]({image})"
                await message.reply(ms_g)
        else:
            await message.reply(ms_g)


@app.on_message(filters.command("char"))
@capture_err
async def character_search(_, message):
    search = message.text.split(' ', 1)
    if len(search) == 1:
        await message.delete()
        return
    search = search[1]
    variables = {'query': search}
    json = requests.post(url, json={'query': character_query, 'variables': variables}).json()[
        'data'].get('Character', None)
    if json:
        ms_g = f"**{json.get('name').get('full')}**(`{json.get('name').get('native')}`)\n"
        description = f"{json['description']}"
        site_url = json.get('siteUrl')
        ms_g += shorten(description, site_url)
        image = json.get('image', None)
        if image:
            image = image.get('large')
            await message.reply_photo(image, caption=ms_g)
        else:
            await message.reply(ms_g)


@app.on_message(filters.command("nhentai"))
@capture_err
async def nhentai(_, message):
    query = message.text.split(" ")[1]
    title, tags, artist, total_pages, post_url, cover_image = nhentai_data(query)
    await message.reply_text(
        f"<code>{title}</code>\n\n<b>Tags:</b>\n{tags}\n<b>Artists:</b>\n{artist}\n<b>Pages:</b>\n{total_pages}",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Read Here",
                        url=post_url
                    )
                ]
            ]
        )
    )


def nhentai_data(noombers):
    url = f"https://nhentai.net/api/gallery/{noombers}"
    res = requests.get(url).json()
    pages = res["images"]["pages"]
    info = res["tags"]
    title = res["title"]["english"]
    links = []
    tags = ""
    artist = ''
    total_pages = res['num_pages']
    extensions = {
        'j':'jpg',
        'p':'png',
        'g':'gif'
    }
    for i, x in enumerate(pages):
        media_id = res["media_id"]
        temp = x['t']
        file = f"{i+1}.{extensions[temp]}"
        link = f"https://i.nhentai.net/galleries/{media_id}/{file}"
        links.append(link)

    for i in info:
        if i["type"]=="tag":
            tag = i['name']
            tag = tag.split(" ")
            tag = "_".join(tag)
            tags+=f"#{tag} "
        if i["type"]=="artist":
            artist=f"{i['name']} "

    post_content = "".join(f"<img src={link}><br>" for link in links)

    post = telegraph.create_page(
        f"{title}",
        html_content=post_content,
        author_name="@WilliamButcherBot", 
        author_url="https://t.me/WilliamButcherBot"
    )
    return title,tags,artist,total_pages,post['url'],links[0]


#Here Comes the Big Bad Thing 

@app.on_message(filters.command(["wa", "tracemoe", "whatanime"]))
@capture_err
async def whatanime(_, message):
    media = message.photo or message.animation or message.video or message.document
    if not media:
        reply = message.reply_to_message
        if not getattr(reply, 'empty', True):
            media = reply.photo or reply.animation or reply.video or reply.document
    if not media:
        await message.reply_text("Gib Me Something, Alteast a Pic, GIF or a Video")
        return
    with tempfile.TemporaryDirectory() as tempdir:
        reply = await message.reply_text('Downloading...')
        path = await app.download_media(media, file_name=os.path.join(tempdir, '0'), progress=progress_callback, progress_args=(reply,))
        new_path = os.path.join(tempdir, '1.png')
        proc = await asyncio.create_subprocess_exec('ffmpeg', '-i', path, '-frames:v', '1', new_path)
        await proc.communicate()
        await reply.edit_text('Uploading...')
        with open(new_path, 'rb') as file:
            async with session.post('https://trace.moe/api/search', data={'image': file}) as resp:
                json = await resp.json()
    if isinstance(json, str):
        await reply.edit_text(html.escape(json))
    else:
        try:
            match = next(iter(json['docs']))
        except StopIteration:
            await reply.edit_text('No match')
        else:
            hentai = match['is_adult']
            title_native = match['title_native']
            title_english = match['title_english']
            title_romaji = match['title_romaji']
            synonyms = ', '.join(match['synonyms'])
            filename = match['filename']
            tokenthumb = match['tokenthumb']
            anilist_id = match['anilist_id']
            episode = match['episode']
            similarity = match['similarity']
            from_time = str(datetime.timedelta(seconds=match['from'])).split('.', 1)[0].rjust(8, '0')
            to_time = str(datetime.timedelta(seconds=match['to'])).split('.', 1)[0].rjust(8, '0')
            at_time = match['at']
            text = f'<a href="https://anilist.co/anime/{anilist_id}">{title_romaji}</a>'
            if title_english:
                text += f' ({title_english})'
            if title_native:
                text += f' ({title_native})'
            if synonyms:
                text += f'\n<b>Synonyms:</b> {synonyms}'
            text += f'\n<b>Similarity:</b> {(Decimal(similarity) * 100).quantize(Decimal(".01"))}%\n'
            if episode:
                text += f'<b>Episode:</b> {episode}\n'
            if hentai:
                text += '<b>Hentai:</b> Yes'
            async def _send_preview():
                url = f'https://media.trace.moe/video/{anilist_id}/{urlencode(filename)}?t={at_time}&token={tokenthumb}'
                with tempfile.NamedTemporaryFile() as file:
                    async with session.get(url) as resp:
                        while True:
                            chunk = await resp.content.read(10)
                            if not chunk:
                                break
                            file.write(chunk)
                    file.seek(0)
                    try:
                        await reply.reply_video(file.name, caption=f'{from_time} - {to_time}')
                    except Exception:
                        await reply.reply_text('Cannot send preview :/')
            await asyncio.gather(reply.edit_text(text, disable_web_page_preview=True), _send_preview())


progress_callback_data = {}


async def progress_callback(current, total, reply):
    message_identifier = (reply.chat.id, reply.message_id)
    last_edit_time, prevtext, start_time = progress_callback_data.get(message_identifier, (0, None, time.time()))
    if current == total:
        try:
            progress_callback_data.pop(message_identifier)
        except KeyError:
            pass
    elif (time.time() - last_edit_time) > 1:
        if last_edit_time:
            download_speed = format_bytes((total - current) / (time.time() - start_time))
        else:
            download_speed = '0 B'
        text = f'''Downloading...
<code>{return_progress_string(current, total)}</code>

<b>Total Size:</b> {format_bytes(total)}
<b>Downladed Size:</b> {format_bytes(current)}
<b>Download Speed:</b> {download_speed}/s
<b>ETA:</b> {calculate_eta(current, total, start_time)}'''
        if prevtext != text:
            await reply.edit_text(text)
            prevtext = text
            last_edit_time = time.time()
            progress_callback_data[message_identifier] = last_edit_time, prevtext, start_time
                    
