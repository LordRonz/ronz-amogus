import aiohttp
from faker import Faker

class Nekoslife:
    __slots__ = ()
    _HOME = 'https://nekos.life/api/v2/img/'
    _fake = Faker().chrome

    def __init__(self):
        pass

    async def get(self, endpoint: str) -> str:
        api = f'{self._HOME}{endpoint}'
        user_agent = self._fake(version_from=80, version_to=86, build_from=4100, build_to=4200)

        async with aiohttp.ClientSession() as session:
            async with session.get(api, headers={'User-agent': user_agent}) as res:
                json = await res.json()

        return json['url']
