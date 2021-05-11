import aiohttp
from faker import Faker

_URL = 'https://dog.ceo/api/breeds/image/random'

async def get_doggo() -> str:
    user_agent = Faker().chrome(version_from=80, version_to=86, build_from=4100, build_to=4200)
    async with aiohttp.ClientSession() as session:
        async with session.get(_URL, headers={'User-agent': user_agent}) as res:
            json: dict = await res.json()
    
    return json['message']
