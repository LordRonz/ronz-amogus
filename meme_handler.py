import requests
from random import randint, choice

SUBREDDITS = ['dankmemes', 'memes']

def isValidImg(url):
    return url.startswith('https://i.') and (url.endswith('.jpg') or url.endswith('.gif') or url.endswith('.png') or url.endswith('.gifv'))

async def get_meme():
    res = requests.get(f'https://www.reddit.com/r/{choice(SUBREDDITS)}/top/.json?sort=top&t=day&showmedia=true&mediaonly=true&is_self=true&limit=69', headers={'User-agent': 'ronz-amogus'})

    url = ''

    json = res.json()['data']['children']
    length = len(json) - 1
    index = 0
    while not isValidImg(url):
        index = randint(0, length)
        url = json[index]['data']['url']

    permalink = f"https://reddit.com{json[index]['data']['permalink']}"
    title = json[index]['data']['title']

    return title, permalink, url
