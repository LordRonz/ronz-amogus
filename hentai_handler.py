from hentai import Hentai, Utils, Format
import requests

def random_hentai(id=None):
    doujin = Hentai(id) if id else Utils.get_random_hentai()
    return doujin.title(Format.Pretty), doujin.url, doujin.image_urls[0]

def check_valid_hentai(embed,inc=True):
    content = embed.image.url
    extension = content.split('/')[-1].split('.')[-1]
    index = int(content.split('/')[-1].replace(f'.{extension}', ''))
    new_index = index + 1 if inc else index - 1
    if new_index <= 0:
        return None
    new_content = f"{'/'.join(content.split('/')[:-1])}/{new_index}.{extension}"
    res = requests.get(new_content, headers={'User-agent': 'ronz-amogus'})
    if res.ok:
        embed.set_image(url=new_content)
        return embed
    else:
        return None
