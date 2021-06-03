from utils.nekoslife import Nekoslife
import aiohttp

class Nekosfun(Nekoslife):
    __slots__ = ()
    _HOME = 'http://api.nekos.fun:8080/api/'

    async def get(self, endpoint: str) -> str:
        api = f'{self._HOME}{endpoint}'
        user_agent = self._fake(version_from=80, version_to=86, build_from=4100, build_to=4200)

        async with aiohttp.ClientSession() as session:
            async with session.get(api, headers={'User-agent': user_agent}) as res:
                json = await res.json()

        return json['image']