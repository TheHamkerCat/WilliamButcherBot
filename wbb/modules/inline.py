from wbb import app
from wbb.utils.inlinefuncs import (
    google_search_func, urban_func, translate_func,
    alive_function, webss, shortify, wall_func,
    saavn_func, deezer_func, inline_help_func,
    torrent_func, youtube_func, lyrics_func,
    paste_func, eval_func, github_user_func,
    github_repo_func, calendar_func, tg_search_func
)
from pyrogram import filters
from pyrogram.errors.exceptions.bad_request_400 import QueryIdInvalid

__MODULE__ = "Inline"
__HELP__ = '''```
- alive - Check Bot's Stats.
- tr [LANG] [QUERY] - Translate Text.
- ud [QUERY] - Urban Dictionary Query.
- google [QUERY] - Google Search.
- webss [URL] - Take Screenshot Of A Website.
- bitly [URL] - Shorten A Link.
- wall [QUERY] - Find Wallpapers.
- saavn [SONG_NAME] - Get Songs From Saavn.
- deezer [SONG_NAME] - Get Songs From Deezer.
- yt [Query] - Youtube Search.
- torrent [QUERY] - Torrent Search.
- lyrics [QUERY] - Lyrics Search.
- calendar - Get Current Month Calendar.
- eval [CODE] - Execute Python Code.
- paste [TEXT] - Paste Text On Pastebin. <=500
- gh_user [USERNAME] - Search A Github User.
- gh_repo [USERNAME/REPO] - Search A Github Repo. 
```'''


@app.on_message(filters.command("inline"))
async def inline_help(_, message):
    await app.send_message(message.chat.id, text=__HELP__)


@app.on_inline_query()
async def inline_query_handler(client, query):
    try:
        text = query.query.lower()
        answers = []
        if text.strip() == '':
            answerss = await inline_help_func(__HELP__)
            await client.answer_inline_query(
                query.id,
                results=answerss,
                cache_time=10
            )
            return
        elif text.split()[0] == "alive":
            answerss = await alive_function(answers)
            await client.answer_inline_query(
                query.id,
                results=answerss,
                cache_time=10
            )
        elif text.split()[0] == "tr":
            lang = text.split()[1]
            tex = text.split(None, 2)[2].strip()
            answerss = await translate_func(answers, lang, tex)
            await client.answer_inline_query(
                query.id,
                results=answerss,
            )
        elif text.split()[0] == "ud":
            tex = text.split(None, 1)[1].strip()
            answerss = await urban_func(answers, tex)
            await client.answer_inline_query(
                query.id,
                results=answerss,
            )
        elif text.split()[0] == "google":
            tex = text.split(None, 1)[1].strip()
            answerss = await google_search_func(answers, tex)
            await client.answer_inline_query(
                query.id,
                results=answerss,
            )
        elif text.split()[0] == "webss":
            tex = text.split(None, 1)[1].strip()
            answerss = await webss(tex)
            await client.answer_inline_query(
                query.id,
                results=answerss,
                cache_time=2
            )
        elif text.split()[0] == "bitly":
            tex = text.split(None, 1)[1].strip()
            answerss = await shortify(tex)
            await client.answer_inline_query(
                query.id,
                results=answerss,
                cache_time=2
            )

        elif text.split()[0] == "wall":
            tex = text.split(None, 1)[1].strip()
            answerss = await wall_func(answers, tex)
            await client.answer_inline_query(
                query.id,
                results=answerss
            )

        elif text.split()[0] == "saavn":
            tex = text.split(None, 1)[1].strip()
            answerss = await saavn_func(answers, tex)
            await client.answer_inline_query(
                query.id,
                results=answerss
            )

        elif text.split()[0] == "deezer":
            tex = text.split(None, 1)[1].strip()
            answerss = await deezer_func(answers, tex)
            await client.answer_inline_query(
                query.id,
                results=answerss
            )

        elif text.split()[0] == "torrent":
            tex = text.split(None, 1)[1].strip()
            answerss = await torrent_func(answers, tex)
            await client.answer_inline_query(
                query.id,
                results=answerss,
            )

        elif text.split()[0] == "yt":
            tex = text.split(None, 1)[1].strip()
            answerss = await youtube_func(answers, tex)
            await client.answer_inline_query(
                query.id,
                results=answerss
            )

        elif text.split()[0] == "lyrics":
            tex = text.split(None, 1)[1].strip()
            answerss = await lyrics_func(answers, tex)
            await client.answer_inline_query(
                query.id,
                results=answerss
            )

        elif text.split()[0] == "eval":
            user_id = query.from_user.id
            tex = text.split(None, 1)[1].strip()
            answerss = await eval_func(answers, tex, user_id)
            await client.answer_inline_query(
                query.id,
                results=answerss,
                cache_time=2
            )

        elif text.split()[0] == "gh_user":
            tex = text.split(None, 1)[1].strip()
            answerss = await github_user_func(answers, tex)
            await client.answer_inline_query(
                query.id,
                results=answerss,
                cache_time=2
            )

        elif text.split()[0] == "gh_repo":
            tex = text.split(None, 1)[1].strip()
            answerss = await github_repo_func(answers, tex)
            await client.answer_inline_query(
                query.id,
                results=answerss,
                cache_time=2
            )

        elif text.split()[0] == "search":
            user_id = query.from_user.id
            tex = text.split(None, 1)[1].strip()
            answerss = await tg_search_func(answers, tex, user_id)
            await client.answer_inline_query(
                query.id,
                results=answerss,
                cache_time=2
            )

    except (IndexError, TypeError, KeyError, ValueError, QueryIdInvalid):
        return
