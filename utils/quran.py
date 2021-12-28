import aiohttp
from faker import Faker
from typing import Union

chrome = Faker().chrome

class Quran:
    __slots__ = (
        'text',
        'arab_text',
        'name',
        'en_name',
        'num',
        'num_in_surah',
    )
    def __init__(
        self,
        text: str,
        arab_text: str,
        name: str,
        en_name: str,
        num: int,
        num_in_surah: int,
    ):
        self.text = (text[:1018] + '...') if len(text) > 1021 else text
        self.arab_text = (arab_text[:1018] + '...') if len(arab_text) > 1021 else arab_text
        self.name = name
        self.en_name = en_name
        self.num = num
        self.num_in_surah = num_in_surah

async def get_quran(ayah: str) -> Union[Quran, None]:
    user_agent = chrome(version_from=80, version_to=86, build_from=4100, build_to=4200)

    url = f'https://api.alquran.cloud/v1/ayah/{ayah}/editions/quran-simple,en.asad'

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers={'User-agent': user_agent}) as res:
            data: dict = await res.json()
    
    if data['code'] != 200 or len(data['data']) != 2:
        return None

    en = data['data'][1]
    ar = data['data'][0]

    return Quran(en['text'], ar['text'], en['surah']['name'], en['surah']['englishName'], int(en['surah']['number']), int(en['numberInSurah']))