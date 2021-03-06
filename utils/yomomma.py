import aiohttp
from faker import Faker

chrome = Faker().chrome

async def get_yomomma() -> str:
    user_agent = chrome(version_from=80, version_to=86, build_from=4100, build_to=4200)
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.yomomma.info/', headers={'User-agent': user_agent}) as res:
            json = await res.json()

    return json['joke']
