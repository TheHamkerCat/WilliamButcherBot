from pyrogram import filters

from wbb.core.decorators.errors import capture_err
from wbb.core.keyboard import ikb
from wbb.utils.http import get
from wbb import app

__MODULE__ = "Crypto"
__HELP__ = '''
/crypto [currency] - Get Real Time value from currency given.
'''

@app.on_message(filters.command('crypto'))
@capture_err
async def crypto(_, message):
    if len(message.command) < 2:
        await message.reply_text("/crypto [currency]")
        return
    
    try:
        if len(message.command) >= 1:
            currency = message.text.split(None, 1)[1]
    except IndexError:
        await message.reply_text('/crypto [currency]')

    currency = currency.lower()
    
    cur = currency.upper()

    btn = ikb({"Available Currency": "https://plotcryptoprice.herokuapp.com"})

    value = ['btc', 'eur', 'idr', 'inr', 'ngn', 'rub','sar', 'try', 'uah', 'usdt', 'wrx']

    msg = await message.reply_text("`Processing...`", quote=True)

    try:
        r = await get("https://x.wazirx.com/wazirx-falcon/api/v2.0/crypto_rates")
        text = f'**Current Crypto Rates For** `{cur}`\n\n'
        for x in value:
            text += f'**Rate to {x.upper()} :** `{r[f"{currency}"][f"{x}"]}`\n'
        await msg.edit(text, reply_markup=btn)
    except KeyError:
        await msg.edit(f'**Invalid Crypto Currency For {cur}**', reply_markup=btn)

