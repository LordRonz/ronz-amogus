from utils.Hentai import Hentai, Utils
from typing import Union

async def random_hentai(id: Union[int, None]=0):
    '''
    Fetch random hentai from nhentai
    '''
    doujin = await Hentai.init(id) if id else await Utils.get_random_hentai()
    
    return doujin
