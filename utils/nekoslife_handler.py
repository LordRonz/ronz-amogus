from utils.nekoslife import Nekoslife

async def get_hentai_gif():
    nekos = Nekoslife('Random_hentai_gif')
    return await nekos.get()

async def get_hentai():
    nekos = Nekoslife('hentai')
    return await nekos.get()
