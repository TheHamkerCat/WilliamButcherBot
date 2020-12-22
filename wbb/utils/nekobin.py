import aiohttp


async def neko(data):
    base_url = "https://nekobin.com"
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{base_url}/api/documents", json={"content": data}, timeout=3
        ) as response:
            key = (await response.json())["result"]["key"]
            reply = f"{base_url}/{key}"
    return reply
