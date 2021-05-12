from utils.Hentai import Hentai, Utils, Format
import aiohttp

EXT = ('jpg', 'png', 'gif')

async def random_hentai(id: int=0):
    '''
    Fetch random hentai from nhentai
    '''
    doujin = await Hentai.init(id) if id else await Utils.get_random_hentai()
    if doujin is None:
        return {}
    title = doujin.title(Format.Pretty)
    url = doujin.url
    img_url = doujin.image_urls[0]
    return {'title': title, 'url': url, 'img_url': img_url}

async def nhentai_update(embed,inc=True):
    content = embed.image.url
    extension = content.split('/')[-1].split('.')[-1]
    index = int(content.split('/')[-1].replace(f'.{extension}', ''))
    new_index = index + 1 if inc else index - 1
    if new_index <= 0:
        return None

    for ext in EXT:
        new_content = f"{'/'.join(content.split('/')[:-1])}/{new_index}.{ext}"
        async with aiohttp.ClientSession() as session:
            async with session.get(new_content, headers={'User-agent': 'ronz-amogus'}) as res:
                if res.status == 200:
                    embed.set_image(url=new_content)
                    return embed
    return None
