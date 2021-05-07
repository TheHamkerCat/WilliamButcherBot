from wbb import app, arq, ARQ_API_BASE_URL
from pyrogram import filters

__MODULE__ = "ARQ"
__HELP__ = "/arq - Stats Of ARQ API."


@app.on_message(filters.command("arq"))
async def arq_stats(_, message):
    data = await arq.stats()
    uptime = data.uptime
    requests = data.requests
    cpu = data.cpu
    server_mem = data.memory.server
    api_mem = data.memory.api
    disk = data.disk
    platform = data.platform
    python_version = data.python
    statistics = f"""
**Uptime:** `{uptime}`
**Requests:** `{requests}`
**CPU:** `{cpu}`
**Memory:**
    **Total Used:** `{server_mem}`
    **Used By API:** `{api_mem}`
**Disk:** `{disk}`
**Platform:** `{platform}`
**Python:** `{python_version}`
"""
    await message.reply_text(statistics)
