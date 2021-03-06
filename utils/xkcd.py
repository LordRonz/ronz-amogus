import aiohttp
from random import randint
from faker import Faker

class XkcdObj:
    __slots__ = (
        'url',
        'title',
        'img',
        'desc',
    )
    def __init__(self, url: str, title: str, img: str, desc: str):
        self.url = url
        self.title = title
        self.img = img
        self.desc = desc
class Xkcd:
    __slots__ = ()
    _URL = 'https://xkcd.com/'
    _TAIL = 'info.0.json'
    _LATEST = f'{_URL}{_TAIL}'
    chrome = Faker().chrome

    def __init__(self):
        pass

    async def get(self) -> XkcdObj:
        user_agent = self.chrome(version_from=80, version_to=86, build_from=4100, build_to=4200)
        headers = {'User-Agent': user_agent}
        async with aiohttp.ClientSession() as session:
            async with session.get(self._LATEST, headers=headers) as res:
                latest = (await res.json())['num']

        rand = Xkcd.get_rand(latest)

        async with aiohttp.ClientSession() as session:
            base_url = f'{self._URL}{rand}/'
            api_url = f'{base_url}{self._TAIL}'
            async with session.get(api_url, headers=headers) as res:
                json = await res.json()
                
        img_url = json['img']
        title = json['title']
        desc = json['alt']

        return XkcdObj(base_url, title, img_url, desc)

    @staticmethod
    def get_rand(latest: int) -> int:
        rand = 404
        while rand == 404:
            rand = randint(1, latest)
        return rand
