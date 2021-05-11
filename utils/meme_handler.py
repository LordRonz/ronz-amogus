from utils.reddit import Reddit
from random import choice

SUBREDDITS = ['dankmemes', 'memes']

async def get_meme():
    reddit = Reddit(choice(SUBREDDITS))

    return await reddit.get()
