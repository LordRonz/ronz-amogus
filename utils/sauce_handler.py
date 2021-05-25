from utils.saucenao.saucenao_api import SauceNao

import os

SAUCENAO_API_KEY = os.getenv('SAUCENAO_API_KEY')

async def get_sauce(url):
    sauce = SauceNao(SAUCENAO_API_KEY)
    return await sauce.from_url(url)
