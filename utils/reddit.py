import aiohttp
from random import randint
from utils.redis_client import redis_client
from datetime import timedelta
import ujson as json

class RedditObj:
    __slots__ = (
        'title',
        'permalink',
        'img',
    )
    def __init__(self, title: str, permalink: str, img: str):
        self.title = title
        self.permalink = permalink
        self.img = img

class Reddit:
    __slots__ = (
        'subreddit',
        'sort',
        'limit',
        'time',
        'url',
    )
    _HOME = 'https://www.reddit.com/'
    def __init__(self, subreddit: str, sort: str='top', limit: int=69, time='day'):
        self.subreddit = subreddit
        self.sort = sort
        self.limit = limit
        self.time = time
        self.url = f'{self._HOME}r/{self.subreddit}/top/.json?sort={self.sort}&t={self.time}&showmedia=true&mediaonly=true&is_self=true&limit={self.limit}'

    async def get(self) -> RedditObj:
        data = None
        cached = await redis_client.r.get(self.subreddit)
        if cached:
            data = json.loads(cached)

        else:
            user_agent = 'ronz-amogus'
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, headers={'User-agent': user_agent}) as res:
                    data = await res.json()
                    data = data['data']['children']
                    await redis_client.r.setex(
                        self.subreddit,
                        timedelta(minutes=69),
                        value=json.dumps(data),
                    )

        index, img_url = self.getImgUrl(data)

        permalink = f"https://reddit.com{data[index]['data']['permalink']}"

        title = data[index]['data']['title']
        return RedditObj(title, permalink, img_url)

    @staticmethod
    def getImgUrl(data: list):
        url = ''
        length = len(data) - 1
        index = 0
        while not (url.startswith('https://i.') and (url.endswith('.jpg') or url.endswith('.gif') or url.endswith('.png') or url.endswith('.gifv'))):
            index = randint(0, length)
            url = data[index]['data']['url']
        return index, url
