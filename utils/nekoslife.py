import aiohttp
from faker import Faker

class Nekoslife(object):
    _HOME = 'https://nekos.life/api/v2/img/'
    _fake = Faker()

    def __init__(self, endpoint: str):
        self.api = f'{self._HOME}{endpoint}'
    
    async def get(self):
        user_agent = self._fake.chrome(version_from=80, version_to=86, build_from=4100, build_to=4200)

        async with aiohttp.ClientSession() as session:
            async with session.get(self.api, headers={'User-agent': user_agent}) as res:
                json = await res.json()

        return json['url']
