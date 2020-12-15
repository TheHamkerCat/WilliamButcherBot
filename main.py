from pyrogram import Client, filters
import random
app = Client("WilliamButcher")


def random_line(fname):
    lines = open(fname).read().splitlines()
    return random.choice(lines)

@app.on_message(filters.command(commands = (["start"])))
async def start(client, message):
    await message.reply_text(random_line('start.txt'))

@app.on_message(filters.command(commands = (["commit"])))
async def commit(client, message):
    await message.reply_text(random_line('commit.txt'))

app.run()