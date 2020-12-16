import aiohttp


async def neko(data):
    BASE_URL = "https://nekobin.com"
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{BASE_URL}/api/documents", json={"content": data}, timeout=3
        ) as response:
            key = (await response.json())["result"]["key"]
            reply = f"{BASE_URL}/{key}"
    return reply
