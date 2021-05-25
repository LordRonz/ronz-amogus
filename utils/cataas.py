import aiohttp
from faker import Faker

_HOME = 'https://cataas.com'
_RANDOM = '/cat?json=true'
chrome = Faker().chrome

async def get_cat() -> str:
    user_agent = chrome(version_from=80, version_to=86, build_from=4100, build_to=4200)
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{_HOME}{_RANDOM}', headers={'User-agent': user_agent}) as res:
            json: dict = await res.json()

    return f'{_HOME}{json["url"]}'