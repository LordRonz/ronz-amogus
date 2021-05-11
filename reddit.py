import aiohttp
from random import randint

class Reddit(object):
    _HOME = 'https://www.reddit.com/'
    def __init__(self, subreddit: str, sort: str='top', limit: int=69):
        self.subreddit = subreddit
        self.sort = sort
        self.limit = limit
        self.url = f'{self._HOME}r/{self.subreddit}/top/.json?sort={self.sort}&t=day&showmedia=true&mediaonly=true&is_self=true&limit={self.limit}'

    async def get(self):
        user_agent = 'ronz-amogus'
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, headers={'User-agent': user_agent}) as res:
                json = await res.json()

        json = json['data']['children']
        length = len(json) - 1
        index = 0

        img_url = ''

        while not Reddit.isValidImg(img_url):
            index = randint(0, length)
            img_url = json[index]['data']['url']

        permalink = f"https://reddit.com{json[index]['data']['permalink']}"

        title = json[index]['data']['title']

        return {'title': title, 'permalink': permalink, 'img': img_url}

    @staticmethod
    def isValidImg(url: str):
        return url.startswith('https://i.') and (url.endswith('.jpg') or url.endswith('.gif') or url.endswith('.png') or url.endswith('.gifv'))
