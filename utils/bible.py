import aiohttp
from faker import Faker
from typing import Union

chrome = Faker().chrome

class Bible:
    __slots__ = (
        'reference',
        'text',
    )
    def __init__(
        self,
        reference: str,
        text: str,
    ):
        self.reference = reference
        self.text = (text[:2040] + '...') if len(text) > 2043 else text

async def get_bible(verse: str) -> Union[Bible, None]:
    user_agent = chrome(version_from=80, version_to=86, build_from=4100, build_to=4200)

    url = f'https://bible-api.com/{verse}?verse_numbers=true&translation=kjv' if verse else 'https://bible-api.com/?random=verse&verse_numbers=true&translation=kjv'

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers={'User-agent': user_agent}) as res:
            data: dict = await res.json()
    
    if 'error' in data:
        return None

    return Bible(data['reference'], data['text'])