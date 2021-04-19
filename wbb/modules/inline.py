from wbb import app
from wbb.utils.inlinefuncs import *
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
- eval [CODE] - Execute Python Code.
- gh_user [USERNAME] - Search A Github User.
- gh_repo [USERNAME/REPO] - Search A Github Repo.
- search [QUERY] - Search For A Message Globally.
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
            if len(text.split()) < 3:
                await client.answer_inline_query(
                    query.id,
                    results=answers,
                    switch_pm_text='Translate Text.',
                    switch_pm_parameter='inline',
                )
                return
            lang = text.split()[1]
            tex = text.split(None, 2)[2].strip()
            answerss = await translate_func(answers, lang, tex)
            await client.answer_inline_query(
                query.id,
                results=answerss,
            )
        elif text.split()[0] == "ud":
            if len(text.split()) < 2:
                await client.answer_inline_query(
                    query.id,
                    results=answers,
                    switch_pm_text='Search Urban Dictionary.',
                    switch_pm_parameter='inline',
                )
                return
            tex = text.split(None, 1)[1].strip()
            answerss = await urban_func(answers, tex)
            await client.answer_inline_query(
                query.id,
                results=answerss,
            )
        elif text.split()[0] == "google":
            if len(text.split()) < 2:
                await client.answer_inline_query(
                    query.id,
                    results=answers,
                    switch_pm_text='Search Google.',
                    switch_pm_parameter='inline',
                )
                return
            tex = text.split(None, 1)[1].strip()
            answerss = await google_search_func(answers, tex)
            await client.answer_inline_query(
                query.id,
                results=answerss,
            )
        elif text.split()[0] == "webss":
            if len(text.split()) < 2:
                await client.answer_inline_query(
                    query.id,
                    results=answers,
                    switch_pm_text='Take Screenshot Of A Website.',
                    switch_pm_parameter='inline',
                )
                return
            tex = text.split(None, 1)[1].strip()
            answerss = await webss(tex)
            await client.answer_inline_query(
                query.id,
                results=answerss,
                cache_time=2
            )
        elif text.split()[0] == "bitly":
            if len(text.split()) < 2:
                await client.answer_inline_query(
                    query.id,
                    results=answers,
                    switch_pm_text='Shorten A Link.',
                    switch_pm_parameter='inline',
                )
                return
            tex = text.split(None, 1)[1].strip()
            answerss = await shortify(tex)
            await client.answer_inline_query(
                query.id,
                results=answerss,
                cache_time=2
            )

        elif text.split()[0] == "wall":
            if len(text.split()) < 2:
                await client.answer_inline_query(
                    query.id,
                    results=answers,
                    switch_pm_text='Search Wallpapers.',
                    switch_pm_parameter='inline',
                )
                return
            tex = text.split(None, 1)[1].strip()
            answerss = await wall_func(answers, tex)
            await client.answer_inline_query(
                query.id,
                results=answerss
            )

        elif text.split()[0] == "saavn":
            if len(text.split()) < 2:
                await client.answer_inline_query(
                    query.id,
                    results=answers,
                    switch_pm_text='Search Songs On JioSaavn.',
                    switch_pm_parameter='inline',
                )
                return
            tex = text.split(None, 1)[1].strip()
            answerss = await saavn_func(answers, tex)
            await client.answer_inline_query(
                query.id,
                results=answerss
            )

        elif text.split()[0] == "deezer":
            if len(text.split()) < 2:
                await client.answer_inline_query(
                    query.id,
                    results=answers,
                    switch_pm_text='Search Songs On Deezer.',
                    switch_pm_parameter='inline',
                )
                return
            tex = text.split(None, 1)[1].strip()
            answerss = await deezer_func(answers, tex)
            await client.answer_inline_query(
                query.id,
                results=answerss
            )

        elif text.split()[0] == "torrent":
            if len(text.split()) < 2:
                await client.answer_inline_query(
                    query.id,
                    results=answers,
                    switch_pm_text='Search For Torrent.',
                    switch_pm_parameter='inline',
                )
                return
            tex = text.split(None, 1)[1].strip()
            answerss = await torrent_func(answers, tex)
            await client.answer_inline_query(
                query.id,
                results=answerss,
            )

        elif text.split()[0] == "yt":
            if len(text.split()) < 2:
                await client.answer_inline_query(
                    query.id,
                    results=answers,
                    switch_pm_text='Search YouTube.',
                    switch_pm_parameter='inline',
                )
                return
            tex = text.split(None, 1)[1].strip()
            answerss = await youtube_func(answers, tex)
            await client.answer_inline_query(
                query.id,
                results=answerss
            )

        elif text.split()[0] == "lyrics":
            if len(text.split()) < 2:
                await client.answer_inline_query(
                    query.id,
                    results=answers,
                    switch_pm_text='Search Lyrics.',
                    switch_pm_parameter='inline',
                )
                return
            tex = text.split(None, 1)[1].strip()
            answerss = await lyrics_func(answers, tex)
            await client.answer_inline_query(
                query.id,
                results=answerss
            )

        elif text.split()[0] == "eval":
            if len(text.split()) < 2:
                await client.answer_inline_query(
                    query.id,
                    results=answers,
                    switch_pm_text='Excute Python Code.',
                    switch_pm_parameter='inline',
                )
                return
            user_id = query.from_user.id
            tex = text.split(None, 1)[1].strip()
            answerss = await eval_func(answers, tex, user_id)
            await client.answer_inline_query(
                query.id,
                results=answerss,
                cache_time=2
            )

        elif text.split()[0] == "gh_user":
            if len(text.split()) < 2:
                await client.answer_inline_query(
                    query.id,
                    results=answers,
                    switch_pm_text='Search Github User.',
                    switch_pm_parameter='inline',
                )
                return
            tex = text.split(None, 1)[1].strip()
            answerss = await github_user_func(answers, tex)
            await client.answer_inline_query(
                query.id,
                results=answerss,
                cache_time=2
            )

        elif text.split()[0] == "gh_repo":
            if len(text.split()) < 2:
                await client.answer_inline_query(
                    query.id,
                    results=answers,
                    switch_pm_text='Search Github Repo.',
                    switch_pm_parameter='inline',
                )
                return
            tex = text.split(None, 1)[1].strip()
            answerss = await github_repo_func(answers, tex)
            await client.answer_inline_query(
                query.id,
                results=answerss,
                cache_time=2
            )

        elif text.split()[0] == "search":
            if len(text.split()) < 2:
                await client.answer_inline_query(
                    query.id,
                    results=answers,
                    switch_pm_text='Global Message Search.',
                    switch_pm_parameter='inline',
                )
                return
            user_id = query.from_user.id
            tex = text.split(None, 1)[1].strip()
            answerss = await tg_search_func(answers, tex, user_id)
            await client.answer_inline_query(
                query.id,
                results=answerss,
                cache_time=2
            )

        elif text.split()[0] == "audio":
            answerss = await cached_audio_test_func(answers)
            await client.answer_inline_query(
                query.id,
                results=answerss,
                cache_time=2
            )

    except (IndexError, TypeError, KeyError, ValueError, QueryIdInvalid) as e:
        print(e + "InLine")
        return
