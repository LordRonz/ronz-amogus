from utils.saucenao.saucenao_api import SauceNao

import os

async def get_sauce(url):
    sauce = SauceNao(os.getenv('SAUCENAO_API_KEY'))
    return await sauce.from_url(url)
