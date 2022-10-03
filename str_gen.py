from pyrogram import Client as c

API_ID = input("\nEnter Your API_ID:\n > ")
API_HASH = input("\nEnter Your API_HASH:\n > ")

print("\n\n Enter Phone number when asked.\n\n")

i = c("wwb", api_id=API_ID, api_hash=API_HASH, in_memory=True)

with i:
    im = i.get_me()
    if im.is_bot:
        print(
            f'Session successfully generated!\n\n{i.export_session_string()}')
    else:
        output = f'**Hi [{im.first_name}](tg://user?id={im.id})\n' \
            f'API_ID:** `{API_ID}`\n**API_HASH:** `{API_HASH}`\n'\
            f'**SESSION:** `{i.export_session_string()}`\n**NOTE: Don\'t give your account information to others!**'
        i.send_message('me', output)
        print('Session successfully generated!\nPlease check your Telegram Saved Messages')
