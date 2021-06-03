from utils.reddit import Reddit
from random import choice

SUBREDDITS = ('dankmemes', 'memes')

async def get_meme():
    reddit = Reddit(choice(SUBREDDITS))

    return await reddit.get()

async def get_agw():
    reddit = Reddit('asiansgonewild', time='week')

    return await reddit.get()

async def get_gw():
    reddit = Reddit('gonewild', time='week')

    return await reddit.get()

async def get_r34():
    reddit = Reddit('rule34')

    return await reddit.get()