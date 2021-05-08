import requests
from random import randint, choice

SUBREDDITS = ['dankmemes', 'memes']

def isValidImg(url):
    return url.startswith('https://i.redd.it') and (url.endswith('.jpg') or url.endswith('.gif') or url.endswith('.png'))

async def get_meme():
    res = requests.get(f'https://www.reddit.com/r/{choice(SUBREDDITS)}/hot/.json?sort=hot&showmedia=true&mediaonly=true&is_self=true&limit=100', headers={'User-agent': 'Amogus'})

    url = ''

    while not isValidImg(url):
        index = randint(0, 101)
        url = res.json()['data']['children'][index]['data']['url']

    return url