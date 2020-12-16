from pyrogram import Client, filters, emoji, types
import random
import time
import shutil, psutil

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


@app.on_message(filters.command(commands = (["ping"])))
def ping(client, message):
    start_time = int(round(time.time() * 1000))
    message.reply_text("Starting Ping")
    end_time = int(round(time.time() * 1000))
    message.reply_text(f'{end_time - start_time} ms')     #Need to edit the above message instead of sending another


@app.on_message(filters.command(commands =(["stats"])))
def stats(client, message):
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    stats = f'<b>CPU:</b> {cpu}% ' \
            f'<b>RAM:</b> {mem}% ' \
            f'<b>Disk:</b> {disk}%'
    message.reply_text(stats)




MESSAGE = "{} Welcome {}!" 

@app.on_message(filters.new_chat_members)
def welcome(client, message):
    new_members = [i.mention for i in message.new_chat_members]
    text = MESSAGE.format(emoji.CROWN, ", ".join(new_members))
    message.reply_text(text, disable_web_page_preview=True)

