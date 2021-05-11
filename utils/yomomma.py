import aiohttp
from faker import Faker

async def get_yomomma():
    user_agent = Faker().chrome(version_from=80, version_to=86, build_from=4100, build_to=4200)
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.yomomma.info/', headers={'User-agent': user_agent}) as res:
            json = await res.json()

    return json['joke']
