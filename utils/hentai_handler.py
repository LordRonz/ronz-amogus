from utils.Hentai import Hentai, Utils

async def random_hentai(id: int=0):
    '''
    Fetch random hentai from nhentai
    '''
    doujin = await Hentai.init(id) if id else await Utils.get_random_hentai()
    
    return doujin
